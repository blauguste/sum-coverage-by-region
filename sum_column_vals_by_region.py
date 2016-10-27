import csv
import sys

coverage_list = []

def sum_range(feature_name, start_pos, end_pos, coverage_list):
    results_tup = ()
    plus_strand_ct = 0
    minus_strand_ct = 0
    length = 0
    for i, row in enumerate(coverage_list):
        if i+1 >= int(start_pos) and i+1 <= int(end_pos):
            plus_strand_ct += int(row[0])
            minus_strand_ct += int(row[1])
            length += 1
    results_tup = (feature_name, plus_strand_ct, minus_strand_ct, length)
    return results_tup

def sum_coverage_per_region(cvg_curve_file_in, loci_table_in, outpath):
    with open(cvg_curve_file_in, 'r') as mapping_file:
        mapping_reader = csv.reader(mapping_file, delimiter='\t')
        for entry in mapping_reader:
            coverage_list.append((int(entry[0]), int(entry[1])))

    loci_list = []
    with open(loci_table_in, 'r') as loci_file:
        loci_reader = csv.reader(loci_file, delimiter=',')
        for row in loci_reader:
            loci_list.append((row[0], row[1], row[2]))

    with open(outpath, 'w') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerow(['feature_name', 'start', 'end', 'plus_reads', 'minus_reads', 'length'])
        for locus in loci_list[1:]:
            strand_sums = sum_range(locus[0], locus[1], locus[2], coverage_list)
            writer.writerow([strand_sums[0], locus[1], locus[2], strand_sums[1], strand_sums[2], strand_sums[3]])

if __name__ == '__main__':
    if len(sys.argv) == 4:
         sum_coverage_per_region(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
         print("Usage: sum_column_vals.py cvg_curve_file_in loci_table_in.csv outpath.csv")
         sys.exit(0)

