import os
import json
import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling
)
import torch
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FineTuner:
    def __init__(self, base_model: str = "microsoft/DialoGPT-medium"):
        """Initialize fine-tuner with base model"""
        self.base_model = base_model
        self.tokenizer = None
        self.model = None
        self.training_args = None
        self.trainer = None
        
    def prepare_training_data(self, conversations: List[Dict[str, str]]) -> Dataset:
        """Prepare conversation data for fine-tuning"""
        formatted_data = []
        
        for conv in conversations:
            # Format as instruction-following data
            instruction = conv.get('instruction', '')
            input_text = conv.get('input', '')
            output = conv.get('output', '')
            
            # Create prompt format
            prompt = f"### Instruction:\n{instruction}\n"
            if input_text:
                prompt += f"### Input:\n{input_text}\n"
            prompt += f"### Response:\n{output}\n### End\n"
            
            formatted_data.append({
                'text': prompt
            })
        
        return Dataset.from_list(formatted_data)
    
    def tokenize_function(self, examples):
        """Tokenize the examples"""
        return self.tokenizer(
            examples["text"],
            truncation=True,
            padding=True,
            max_length=512,
            return_tensors="pt"
        )
    
    def initialize_model(self):
        """Initialize the model and tokenizer"""
        logger.info(f"Loading model: {self.base_model}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.base_model)
        self.model = AutoModelForCausalLM.from_pretrained(self.base_model)
        
        # Add padding token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Resize token embeddings
        self.model.resize_token_embeddings(len(self.tokenizer))
        
        logger.info("Model and tokenizer initialized successfully")
    
    def setup_training(self, output_dir: str = "./fine_tuned_model"):
        """Setup training arguments and trainer"""
        self.training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            eval_steps=400,
            save_steps=800,
            warmup_steps=500,
            prediction_loss_only=True,
            logging_dir=f"{output_dir}/logs",
            logging_steps=100,
            save_total_limit=2,
            load_best_model_at_end=True,
            evaluation_strategy="steps",
            learning_rate=5e-5,
            weight_decay=0.01,
            fp16=True if torch.cuda.is_available() else False,
        )
        
        logger.info("Training arguments configured")
    
    def train(self, training_data: Dataset, output_dir: str = "./fine_tuned_model"):
        """Train the model"""
        if self.model is None or self.tokenizer is None:
            self.initialize_model()
        
        if self.training_args is None:
            self.setup_training(output_dir)
        
        # Tokenize the dataset
        tokenized_dataset = training_data.map(
            self.tokenize_function,
            batched=True,
            remove_columns=training_data.column_names
        )
        
        # Setup data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        # Initialize trainer
        self.trainer = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=tokenized_dataset,
            data_collator=data_collator,
        )
        
        logger.info("Starting training...")
        self.trainer.train()
        
        # Save the model
        self.trainer.save_model()
        self.tokenizer.save_pretrained(output_dir)
        
        logger.info(f"Training completed. Model saved to {output_dir}")
        
        return output_dir
    
    def generate_response(self, prompt: str, max_length: int = 100) -> str:
        """Generate response using the fine-tuned model"""
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model not initialized. Please train or load a model first.")
        
        # Tokenize input
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        
        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove the input prompt from response
        response = response[len(prompt):].strip()
        
        return response
    
    def load_model(self, model_path: str):
        """Load a fine-tuned model"""
        logger.info(f"Loading model from {model_path}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        logger.info("Model loaded successfully")
    
    def create_training_data_from_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Create training data from document Q&A pairs"""
        training_data = []
        
        for doc in documents:
            # Create instruction-following format from document content
            instruction = "Answer the following question based on the provided document."
            input_text = f"Document: {doc.get('document', '')}\nQuestion: {doc.get('question', '')}"
            output = doc.get('answer', '')
            
            training_data.append({
                'instruction': instruction,
                'input': input_text,
                'output': output
            })
        
        return training_data
    
    def evaluate_model(self, test_data: List[Dict[str, str]]) -> Dict[str, float]:
        """Evaluate the fine-tuned model"""
        if self.model is None:
            raise ValueError("Model not initialized")
        
        # Prepare test dataset
        test_dataset = self.prepare_training_data(test_data)
        tokenized_test = test_dataset.map(
            self.tokenize_function,
            batched=True,
            remove_columns=test_dataset.column_names
        )
        
        # Evaluate
        eval_results = self.trainer.evaluate(tokenized_test)
        
        return {
            'eval_loss': eval_results['eval_loss'],
            'eval_perplexity': torch.exp(torch.tensor(eval_results['eval_loss'])).item()
        }

# Global instance
fine_tuner = FineTuner() 