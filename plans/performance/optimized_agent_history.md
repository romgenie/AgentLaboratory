# Optimized Agent History Management

## Overview
The current implementation of history management in the BaseAgent class uses inefficient data structures and operations, which causes performance degradation, especially with longer conversations. This plan outlines improvements to make history management more efficient.

## Problem
- Current implementation uses lists for history with O(n) complexity for removing elements
- Fixed history size (max_hist_len = 15) regardless of message content size
- Inefficient handling of expired messages
- No compression or trimming of message content
- Memory usage grows linearly with conversation length

## Solution
Implement a more efficient history management system:
1. Use collections.deque for O(1) operations at both ends
2. Implement intelligent message trimming
3. Add content-aware history management
4. Optimize context retrieval

## Implementation Steps

### 1. Replace List with Deque
```python
from collections import deque

class BaseAgent:
    def __init__(self, name, role_desc, llm_config):
        # ... existing initialization ...
        
        # Use deque instead of list for efficient operations
        self.max_hist_len = 15
        self.history = deque(maxlen=self.max_hist_len)
        
        # ... rest of initialization ...
```

### 2. Improve Message Storage
```python
class BaseAgent:
    # ... existing code ...
    
    def add_message(self, role, content, expires=False, max_tokens=None):
        """Add a message to the agent's history with optional intelligent trimming"""
        if max_tokens and content:
            # Calculate approximate token length
            token_length = len(content.split())
            
            # If content exceeds max_tokens, trim it intelligently
            if token_length > max_tokens:
                # For code, preserve structure but trim
                if "```" in content:
                    # Preserve code blocks but trim them
                    content = self._trim_code_blocks(content, max_tokens)
                else:
                    # For regular text, keep important parts
                    sentences = content.split(". ")
                    if len(sentences) > 3:
                        # Keep first sentence, some middle, and last sentence
                        keep_count = min(max_tokens // 20, len(sentences))
                        content = ". ".join(
                            [sentences[0]] + 
                            sentences[1:keep_count-1] + 
                            [sentences[-1]]
                        )
        
        # Add the message to history using deque's efficient append
        self.history.append({
            "role": role,
            "content": content,
            "expires": expires,
            "timestamp": time.time()
        })
        
        # No need to manually manage length - deque handles it automatically
```

### 3. Optimize Context Retrieval
```python
class BaseAgent:
    # ... existing code ...
    
    def context(self):
        """Return the conversation context more efficiently"""
        # Create a list of active messages
        messages = []
        
        # Get current system prompt
        messages.append({
            "role": "system", 
            "content": self.system_prompt()
        })
        
        # Add non-expired messages from history
        for msg in self.history:
            if not msg.get("expires", False):
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        return messages
    
    def _trim_code_blocks(self, content, max_tokens):
        """Intelligently trim code blocks while preserving structure"""
        # Split into code and non-code segments
        segments = []
        in_code_block = False
        current_segment = ""
        
        for line in content.split("\n"):
            if line.startswith("```"):
                # Toggle code block state
                if current_segment:
                    segments.append((in_code_block, current_segment))
                    current_segment = ""
                in_code_block = not in_code_block
                current_segment += line + "\n"
            else:
                current_segment += line + "\n"
                
        if current_segment:
            segments.append((in_code_block, current_segment))
        
        # Estimate tokens and trim while preserving structure
        total_tokens = sum(len(segment[1].split()) for segment in segments)
        if total_tokens <= max_tokens:
            return content
            
        # Calculate how much to keep
        keep_ratio = max_tokens / total_tokens
        
        # Trim each segment proportionally
        result = ""
        for is_code, segment in segments:
            if is_code:
                # Preserve code structure but limit lines
                code_lines = segment.split("\n")
                if len(code_lines) > 5:
                    # Keep start markers, first few lines, and end markers
                    result += "\n".join(code_lines[:2])  # Start of code block
                    result += "\n# ... [code trimmed for brevity] ...\n"
                    result += "\n".join(code_lines[-2:])  # End of code block
                else:
                    result += segment
            else:
                # Trim text proportionally
                words = segment.split()
                keep_words = max(3, int(len(words) * keep_ratio))
                result += " ".join(words[:keep_words])
                if keep_words < len(words):
                    result += " ... [text trimmed] "
                    
        return result
```

### 4. Add Message Expiration Management
```python
class BaseAgent:
    # ... existing code ...
    
    def clean_expired_messages(self, expiration_time=3600):
        """Remove expired messages older than expiration_time seconds"""
        current_time = time.time()
        
        # Filter out expired messages older than expiration_time
        self.history = deque(
            [msg for msg in self.history 
             if not (msg.get("expires", False) and 
                    current_time - msg.get("timestamp", 0) > expiration_time)],
            maxlen=self.max_hist_len
        )
```

## Benefits
- Improved performance with O(1) operations for history management
- Reduced memory usage through intelligent content trimming
- Better preservation of important content
- More flexible history size based on content importance
- Simplified code with fewer manual operations

## Metrics for Success
- 30%+ reduced memory footprint for agent history
- Faster history operations (measurable in microseconds)
- No loss of critical conversation context despite trimming
- Better handling of long-running conversations