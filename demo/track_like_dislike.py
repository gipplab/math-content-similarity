import json
import csv

def load_matomo_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def process_log_data(data):
    results = []
    for entry in data:
        visitor_id = entry.get('visitorId', 'unknown')
        for action in entry.get('actionDetails', []):
            url = action.get('url', '')
            if url and 'reaction' in url and 'target' in url:
                reaction = 'like' if 'reaction=like' in url else 'dislike' if 'reaction=dislike' in url else ''
                if reaction:
                    seed_start = url.find("Publication:") + len("Publication:")
                    seed_end = url.find("?", seed_start)
                    seed = url[seed_start:seed_end] if seed_end != -1 else url[seed_start:]
                    target_start = url.find("target=") + len("target=")
                    target_end = url.find("&", target_start)
                    target = url[target_start:target_end] if target_end != -1 else url[target_start:]
                    results.append([seed, target, reaction, visitor_id])
    return results

# Write the results to a CSV file
def write_to_csv(results, output_file_path):
    with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['seed', 'recommendation', 'like or dislike', 'user_id'])
        writer.writerows(results)

def main():
    input_file = 'logs_mat.json'
    output_file = 'visitor_log_reactions_with_visitor_id.csv'
    data = load_matomo_data(input_file)
    results = process_log_data(data)
    write_to_csv(results, output_file)
    print(f"Results saved to {output_file}")

# Run the main function
if __name__ == "__main__":
    main()
