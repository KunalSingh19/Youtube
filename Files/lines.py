input_file = 'input.txt'   # your messed up file
output_file = 'output.txt' # cleaned output file

with open(input_file, 'r') as f:
    content = f.read()

# Split links by whitespace
links = content.split()

# Write all links one per line
with open(output_file, 'w') as f:
    for link in links:
        f.write(link + '\n')

print(f"Processed {len(links)} links. Output saved to {output_file}")
