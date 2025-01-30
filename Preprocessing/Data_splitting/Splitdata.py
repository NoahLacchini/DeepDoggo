def write_sequence_to_file(sequence, output_file):
    if len(sequence) >= 50:
        start = 0
        while start + 50 <= len(sequence):
            output_file.write(sequence[start:start+50] + "\n")
            start += 2

def process_fasta_file(filename):
    with open(filename, "r") as fasta_file, open("output5.txt", "w") as output_file:
        current_sequence = ""
        for line in fasta_file:
            line = line.strip()
            if line.startswith(">"):
                if current_sequence:
                    write_sequence_to_file(current_sequence, output_file)
                    current_sequence = ""
            else:
                current_sequence += line

        if current_sequence:
            write_sequence_to_file(current_sequence, output_file)

# Replace 'input.fasta' with the path to your FASTA file
process_fasta_file('data/viral2.txt')
