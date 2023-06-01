
#!/bin/bash

# Directory path where the samples are located
input_directory="directory/mapped"

# Directory path for the output files
output_directory="directory/unmapped"

# Loop through each file in the input directory
for file in "$input_directory"/*_mapped_and_unmapped.bam.gz; do
    # Extract the sample name from the file name
    sample=$(basename "$file" | cut -d "" -f 1)

# Construct the output file path
    output_file="${output_directory}/${sample}_bothEndsUnmapped.bam.gz"

# Run the samtools command
    samtools view -b -f 12 -F 256 "$file" > "$output_file"

# Print a message indicating completion for each sample
    echo "Conversion completed for $sample"
done
