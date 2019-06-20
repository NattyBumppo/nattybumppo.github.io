import os
import subprocess
import csv

csv_filename = 'vocab.csv'
temp_csv_filename = 'temp_vocab.csv'
html_filename = 'index.html'
html_gen_cl = 'csvtotable %s %s --overwrite --caption "語彙リスト" --pagination --export-options copy --export-options csv --export-options json --export-options print' % (temp_csv_filename, html_filename)

# Import csv
with open(csv_filename, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

    with open(temp_csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # Add bold formatting to word
            word = row['Word']
            emboldened_word = '<strong>%s</strong>' % row['Word']
            row['Word'] = '<strong>%s</strong>' % word

            # Divide slash-delimited synonyms into lines
            synonyms = row['Synonym(s)'].split('/')
            row['Synonym(s)'] = '<ul><li>' + '</li><li>'.join(synonyms) + '</li></ul>'

            # Divide slash-delimited sample sentences into lines
            sentences = row['Sample Sentences (JP)'].split('/')
            row['Sample Sentences (JP)'] = '<ol><li>' + '</li><li>'.join(sentences) + '</li></ol>'
        
            sentences = row['Sample Sentences (EN)'].split('/')
            row['Sample Sentences (EN)'] = '<ol><li>' + '</li><li>'.join(sentences) + '</li></ol>'

            # Add bold formatting to word in sample sentences
            row['Sample Sentences (JP)'] = row['Sample Sentences (JP)'].replace(word, emboldened_word)
        
            # Output modified row to temporary file
            writer.writerow(row)

# Make output html
return_code = int(subprocess.call(html_gen_cl, shell=True))
if return_code != 0:
    print('HTML generation returned with %s.' % return_code)

# Delete temp csv file
os.remove(temp_csv_filename)