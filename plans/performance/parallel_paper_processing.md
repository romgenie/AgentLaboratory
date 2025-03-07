# Parallel Paper Processing Implementation

## Overview
The current implementation of paper downloading, processing, and analysis in the literature review phase is performed sequentially, which significantly slows down the research process. This plan outlines the implementation of parallel processing for papers to speed up the literature review phase.

## Problem
- Papers are processed one at a time in ArxivSearch and SemanticScholarSearch
- Fixed sleep delays after each paper operation waste time
- PDF downloads and text extraction is sequential and CPU-bound
- Literature review phase is one of the most time-consuming parts of the research workflow

## Solution
Implement parallel processing of papers using Python's concurrent.futures module:
1. Concurrent API requests with proper rate limiting
2. Parallel PDF downloads and text extraction
3. Asynchronous paper analysis

## Implementation Steps

### 1. Modify ArxivSearch for Parallel Processing
```python
import concurrent.futures
from functools import partial
import time
import backoff

class ArxivSearch:
    def __init__(self, max_workers=5):
        self.sch_engine = arxiv.Client()
        self.max_workers = max_workers
        
    # Exponential backoff retry decorator for API rate limits
    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=3,
        max_time=30
    )
    def _get_single_paper(self, paper_result):
        """Process a single paper result"""
        paperid = paper_result.pdf_url.split("/")[-1]
        pubdate = str(paper_result.published).split(" ")[0]
        paper_sum = f"Title: {paper_result.title}\n"
        paper_sum += f"Summary: {paper_result.summary}\n"
        paper_sum += f"Publication Date: {pubdate}\n"
        paper_sum += f"Categories: {' '.join(paper_result.categories)}\n"
        paper_sum += f"arXiv paper ID: {paperid}\n"
        return paper_sum
        
    def find_papers_by_str(self, query, N=20):
        processed_query = self._process_query(query)
        
        try:
            search = arxiv.Search(
                query="abs:" + processed_query,
                max_results=N,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            # Get all results first (this is quick and doesn't count towards rate limits)
            results = list(self.sch_engine.results(search))
            
            # Process results in parallel with proper throttling
            paper_sums = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all tasks
                future_to_paper = {
                    executor.submit(self._get_single_paper, paper): paper 
                    for paper in results
                }
                
                # Process results as they complete
                for future in concurrent.futures.as_completed(future_to_paper):
                    try:
                        paper_sum = future.result()
                        paper_sums.append(paper_sum)
                    except Exception as e:
                        print(f"Error processing paper: {e}")
            
            return "\n".join(paper_sums)
                
        except Exception as e:
            print(f"Error in arxiv search: {e}")
            return None
```

### 2. Implement Parallel PDF Processing
```python
class ArxivSearch:
    # ... existing code ...
    
    def _download_and_extract(self, paper_id):
        """Download and extract text from a single paper"""
        try:
            # Get paper
            paper = next(arxiv.Client().results(arxiv.Search(id_list=[paper_id])))
            
            # Create temp filename with the paper ID to avoid conflicts
            filename = f"temp_paper_{paper_id.replace('/', '_')}.pdf"
            
            # Download the PDF
            paper.download_pdf(filename=filename)
            
            try:
                # Extract text
                reader = PdfReader(filename)
                pdf_text = ""
                
                for page_number, page in enumerate(reader.pages, start=1):
                    try:
                        text = page.extract_text()
                        pdf_text += f"--- Page {page_number} ---"
                        pdf_text += text
                        pdf_text += "\n"
                    except Exception as e:
                        pdf_text += f"[Error extracting page {page_number}: {str(e)}]\n"
                
                return pdf_text
            finally:
                # Clean up the file regardless of success or failure
                try:
                    os.remove(filename)
                except:
                    pass
                    
        except Exception as e:
            return f"EXTRACTION FAILED: {str(e)}"
    
    def retrieve_multiple_papers(self, paper_ids):
        """Download and process multiple papers in parallel"""
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all paper downloads
            future_to_id = {
                executor.submit(self._download_and_extract, paper_id): paper_id
                for paper_id in paper_ids
            }
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_id):
                paper_id = future_to_id[future]
                try:
                    text = future.result()
                    results[paper_id] = text
                except Exception as e:
                    results[paper_id] = f"ERROR: {str(e)}"
        
        return results
```

### 3. Modify Literature Review Phase
Update the literature_review.py file to use the new parallel methods:

```python
def literature_review(self, arxiv_search, semantic_scholar_search):
    # Existing code to get queries...
    
    # Instead of sequential processing:
    paper_ids = []  # Collect paper IDs from search results
    
    # Get paper IDs from search results
    search_results = arxiv_search.find_papers_by_str(query, N=20)
    for result in parse_search_results(search_results):
        paper_ids.append(result['paper_id'])
    
    # Process papers in parallel
    paper_texts = arxiv_search.retrieve_multiple_papers(paper_ids)
    
    # Continue with analysis...
```

## Benefits
- Significant reduction in literature review time (potentially 3-5x speedup)
- More efficient use of API rate limits with proper backoff
- Better error handling and recovery for individual paper failures
- Improved user experience with faster initial results

## Metrics for Success
- 70%+ reduction in total time for literature review phase
- Processing at least 5 papers concurrently
- Proper error handling that doesn't halt the entire process if a single paper fails
- Graceful degradation under API rate limiting