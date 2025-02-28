import os
import socket
from collections import Counter

def expand_contractions(text):
    contractions_dict = {
        "I'm": "I am",
        "I'll": "I will",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "don't": "do not",
        "you're": "you are",
        "wanna": "want to",
        "that's": "that is",
        "it's": "it is",
    }

    for contraction, full_form in contractions_dict.items():
        text = text.replace(contraction, full_form)
    
    return text

def process_file_content(file_path, split_contractions_flag=False):
    try:
        with open(file_path, 'r') as file:
            text = file.read()

        total_words_before_split = len(text.split())

        if split_contractions_flag:
            text = expand_contractions(text)

        words = text.split()

        word_counts = Counter(words)

        return total_words_before_split, word_counts

    except FileNotFoundError as e:
        print(f"File not found: {file_path}")
        return 0, Counter()
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return 0, Counter()

def write_results_to_file(results):
    output_dir = '/home/data/output'

    os.makedirs(output_dir, exist_ok=True)
    
    result_file_path = os.path.join(output_dir, 'result.txt')

    try:
        with open(result_file_path, 'w') as result_file:
            result_file.write(results)
        print(f"Results written to {result_file_path}") 
    except Exception as e:
        print(f"Error writing results: {e}")

    return result_file_path

def get_ip_address():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        print(f"Error getting IP address: {e}")
        return "Unknown"

def main():
    try:
        if_file_path = '/home/data/IF.txt' 
        always_remember_file_path = '/home/data/AlwaysRememberUsThisWay.txt'  # Path to AlwaysRememberUsThisWay.txt inside the container

        total_words_if, word_counts_if = process_file_content(if_file_path)
        top_3_if = word_counts_if.most_common(3)

        total_words_always_remember_before, word_counts_always_remember = process_file_content(always_remember_file_path, split_contractions_flag=True)
        top_3_always_remember = word_counts_always_remember.most_common(3)

        grand_total_words = total_words_if + total_words_always_remember_before

        ip_address = get_ip_address()

        results = (
            "Results for IF.txt:\n"
            f"Total words: {total_words_if}\n"
            "Top 3 most frequent words:\n"
        )
        for word, count in top_3_if:
            results += f"{word}: {count}\n"

        results += (
            "\nResults for AlwaysRememberUsThisWay.txt:\n"
            f"Total words before splitting contractions: {total_words_always_remember_before}\n"
            "Top 3 most frequent words:\n"
        )
        for word, count in top_3_always_remember:
            results += f"{word}: {count}\n"

        results += f"\nGrand total of words across both files: {grand_total_words}\n"
        results += f"IP Address of the container: {ip_address}\n"

        result_file_path = write_results_to_file(results)

        with open(result_file_path, 'r') as result_file:
            print(result_file.read())

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
