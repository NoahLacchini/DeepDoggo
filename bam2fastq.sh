#!/bin/bash

# List of sample names
samples=(
"Samples_names"
)

# Directory paths
input_dir="directory/umapped/sorted"
output_dir="directory/unmapped/sorted"

# Loop through each sample
for sample in "${samples[@]}"; do
    # Input and output file paths
    input_file="$input_dir/${sample}_bothEndsUnmapped_sorted.bam"
    output_file_r1="$output_dir/${sample}_host_removed_r1.fastq"
    output_file_r2="$output_dir/${sample}_host_removed_r2.fastq"

   # Run the bedtools bamtofastq command
    bedtools bamtofastq -i "$input_file" -fq "$output_file_r1" -fq2 "$output_file_r2"

    # Print a message indicating completion for each sample
    echo "Conversion completed for $sample"

done
