genome_file = "/home/zaamos/Bureau/data_deep/chien/chien_ref.fasta"  # Replace with the path to your genome FASTA file
chunk_size = 10000000  # Chunk size in base pairs (adjust for optimal performance)

output_file = "/home/zaamos/Bureau/data_deep/chien/genome_sequences.txt"  # Path to the output text file

# Open the output file in write mode
with open(output_file, "w") as f_out:
    # Read the genome file
    with open(genome_file, "r") as f_in:
        sequence = ""
        for line in f_in:
            if line.startswith(">"):
                # Process the previous sequence chunk
                for i in range(0, len(sequence), 50):
                    chunk = sequence[i:i+50]
                    f_out.write(chunk + "\n")

                # Start a new sequence
                sequence = ""
            else:
                # Concatenate the sequence lines
                sequence += line.strip()

        # Process the last sequence chunk
        for i in range(0, len(sequence), 50):
            chunk = sequence[i:i+50]
            f_out.write(chunk + "\n")
