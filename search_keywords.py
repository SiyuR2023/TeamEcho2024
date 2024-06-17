import os
import re
import json

def load_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def search_keywords(text_lines, keywords, page_num):
    results = []
    for i, line in enumerate(text_lines):
        for keyword in keywords:
            if keyword.lower() in line.lower():
                results.append((keyword, i, line.strip(), page_num))
    return results

def extract_value(text_lines, index):
    if 0 <= index < len(text_lines):
        return text_lines[index].strip()
    return "unknown"

def process_files(text_files, keywords, value_index):
    results = {}
    page_num = 1  # Initialize page number

    for text_file in text_files:
        file_name = os.path.basename(text_file)
        text_lines = load_text_file(text_file)
        
        keyword_hits = []
        
        for i, line in enumerate(text_lines):
            for keyword in keywords:
                if keyword.lower() in line.lower():
                    keyword_hits.append((keyword, i, line.strip(), page_num))
                    page_num += 1  # Increment page number for each keyword hit
        
        if keyword_hits:
            file_results = []
            for keyword, keyword_index, line, page_num in keyword_hits:
                value = extract_value(text_lines, keyword_index + value_index)
                file_results.append({
                    'keyword': keyword,
                    'keyword_index': keyword_index,
                    'line': line,
                    'value': value,
                    'page_num': page_num
                })
            results[file_name] = file_results

    return results

def save_results_to_file(results, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4)

if __name__ == "__main__":
    # Directory containing extracted text files
    text_files_dir = 'extracted_texts'
    output_file = 'search_results.json'
    
    # Prompt the user for keywords and value index
    keywords = input("Enter keywords to search for (comma-separated): ").split(',')
    keywords = [keyword.strip() for keyword in keywords]
    value_index = int(input("Enter the value index relative to the keyword: "))
    
    # Get list of text files
    text_files = [os.path.join(text_files_dir, f) for f in os.listdir(text_files_dir) if f.endswith('.txt')]
    
    # Process files
    results = process_files(text_files, keywords, value_index)
    
    # Save results
    save_results_to_file(results, output_file)
    
    print(f"Search results saved to {output_file}")
