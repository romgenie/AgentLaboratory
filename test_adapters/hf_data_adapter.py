"""
Hugging Face data search adapter for tests.

This module provides adapter functions for the hf_data_search functionality
that tests expect, without modifying the original code.
"""

import sys
import os

# Add project root to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Create mock implementation for testing without API calls
def search_hf_datasets(query, max_results=5):
    """
    Mock implementation of search_hf_datasets that doesn't require API access.
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results
        
    Returns:
        list: List of dataset data with predefined test results
    """
    # Test data for datasets
    test_data = [
        {
            'id': 'mnist',
            'title': 'MNIST',
            'description': 'The MNIST database of handwritten digits.',
            'tags': ['vision', 'classification', 'image'],
            'downloads': 1500000,
            'likes': 750
        },
        {
            'id': 'glue',
            'title': 'GLUE Benchmark',
            'description': 'General Language Understanding Evaluation benchmark.',
            'tags': ['nlp', 'benchmark', 'text-classification'],
            'downloads': 950000,
            'likes': 500
        },
        {
            'id': 'squad',
            'title': 'SQuAD: Stanford Question Answering Dataset',
            'description': 'Stanford Question Answering Dataset (SQuAD) is a reading comprehension dataset.',
            'tags': ['nlp', 'question-answering', 'reading-comprehension'],
            'downloads': 850000,
            'likes': 430
        },
        {
            'id': 'coco',
            'title': 'COCO: Common Objects in Context',
            'description': 'COCO is a large-scale object detection, segmentation, and captioning dataset.',
            'tags': ['vision', 'object-detection', 'image-segmentation'],
            'downloads': 750000,
            'likes': 380
        },
        {
            'id': 'wmt',
            'title': 'WMT: Machine Translation',
            'description': 'Shared task datasets from the Conference on Machine Translation (WMT).',
            'tags': ['nlp', 'translation', 'machine-translation'],
            'downloads': 550000,
            'likes': 290
        }
    ]
    
    # Filter results based on query
    if query:
        filtered_results = [
            dataset for dataset in test_data 
            if query.lower() in dataset['title'].lower() or 
               query.lower() in dataset['description'].lower() or
               any(query.lower() in tag.lower() for tag in dataset['tags'])
        ]
    else:
        filtered_results = test_data
    
    # Return up to max_results
    return filtered_results[:max_results]

def search_hf_models(query, max_results=5):
    """
    Mock implementation of search_hf_models that doesn't require API access.
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results
        
    Returns:
        list: List of model data with predefined test results
    """
    # Test data for models
    test_data = [
        {
            'id': 'bert-base-uncased',
            'title': 'BERT base model (uncased)',
            'description': 'BERT base model with 12 layers and 110M parameters.',
            'tags': ['nlp', 'transformers', 'text-classification'],
            'downloads': 8500000,
            'likes': 1200
        },
        {
            'id': 'gpt2',
            'title': 'GPT-2',
            'description': 'OpenAI GPT-2 language model with 117M parameters.',
            'tags': ['nlp', 'text-generation', 'language-modeling'],
            'downloads': 7500000,
            'likes': 1100
        },
        {
            'id': 'resnet-50',
            'title': 'ResNet-50',
            'description': 'ResNet model with 50 layers for image classification.',
            'tags': ['vision', 'image-classification', 'cnn'],
            'downloads': 6500000,
            'likes': 950
        },
        {
            'id': 't5-base',
            'title': 'T5 Base',
            'description': 'Text-to-Text Transfer Transformer model with 220M parameters.',
            'tags': ['nlp', 'transformers', 'text-to-text'],
            'downloads': 5500000,
            'likes': 850
        },
        {
            'id': 'yolov5',
            'title': 'YOLOv5',
            'description': 'YOLOv5 for object detection tasks in computer vision.',
            'tags': ['vision', 'object-detection', 'yolo'],
            'downloads': 4500000,
            'likes': 750
        }
    ]
    
    # Filter results based on query
    if query:
        filtered_results = [
            model for model in test_data 
            if query.lower() in model['title'].lower() or 
               query.lower() in model['description'].lower() or
               any(query.lower() in tag.lower() for tag in model['tags'])
        ]
    else:
        filtered_results = test_data
    
    # Return up to max_results
    return filtered_results[:max_results]

class HuggingFaceEngine:
    """
    Mock Hugging Face engine that simulates API access for testing.
    """
    
    def __init__(self):
        """Initialize the Hugging Face engine."""
        self.datasets = {
            'mnist': {'splits': ['train', 'test'], 'num_samples': 70000},
            'glue': {'splits': ['train', 'validation', 'test'], 'num_samples': 150000},
            'squad': {'splits': ['train', 'validation'], 'num_samples': 100000},
            'coco': {'splits': ['train', 'validation'], 'num_samples': 200000},
            'wmt': {'splits': ['train', 'validation', 'test'], 'num_samples': 250000}
        }
        
        self.models = {
            'bert-base-uncased': {'parameters': 110000000, 'architecture': 'Transformer encoder'},
            'gpt2': {'parameters': 117000000, 'architecture': 'Transformer decoder'},
            'resnet-50': {'parameters': 25000000, 'architecture': 'CNN'},
            't5-base': {'parameters': 220000000, 'architecture': 'Transformer encoder-decoder'},
            'yolov5': {'parameters': 85000000, 'architecture': 'CNN'}
        }
    
    def get_dataset_details(self, dataset_id):
        """
        Retrieve details about a dataset by its ID.
        
        Args:
            dataset_id (str): ID of the dataset
            
        Returns:
            dict: Details of the dataset
        """
        if dataset_id in self.datasets:
            datasets = search_hf_datasets("")
            for dataset in datasets:
                if dataset['id'] == dataset_id:
                    return {
                        **dataset,
                        **self.datasets[dataset_id]
                    }
        
        return {'error': f"Dataset with ID {dataset_id} not found"}
    
    def get_model_details(self, model_id):
        """
        Retrieve details about a model by its ID.
        
        Args:
            model_id (str): ID of the model
            
        Returns:
            dict: Details of the model
        """
        if model_id in self.models:
            models = search_hf_models("")
            for model in models:
                if model['id'] == model_id:
                    return {
                        **model,
                        **self.models[model_id]
                    }
        
        return {'error': f"Model with ID {model_id} not found"}
    
    def search_datasets(self, query, max_results=5):
        """
        Search for datasets on Hugging Face.
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results
            
        Returns:
            list: List of dataset data
        """
        return search_hf_datasets(query, max_results)
    
    def search_models(self, query, max_results=5):
        """
        Search for models on Hugging Face.
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results
            
        Returns:
            list: List of model data
        """
        return search_hf_models(query, max_results)

# Export the functions and classes
__all__ = ['search_hf_datasets', 'search_hf_models', 'HuggingFaceEngine']