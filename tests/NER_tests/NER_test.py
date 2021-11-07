import requests
import json

server_url = 'http://127.0.0.1:5000'
headers = {'Content-Type': 'application/json', 'Accept':'application/json'}

#Test searching desiace entities in text
#text from https://arxiv.org/ftp/arxiv/papers/2110/2110.12723.pdf
data = {"text": '''The increasing prevalence of SAS-CoV-2 variants with spike mutations has raised concerns
owing to higher transmission rates, disease severity, and escape from neutralizing antibodies. apid and accurate detection of SAS-CoV-2 variants provides crucial information concerning
the outbreaks of SAS-CoV-2 variants and possible lines of transmission. This information is vital
for infection prevention and control. We used a Cas12a-based T-PC combined with CISP
on-site rapid detection system (T-CODS) platform to detect the key mutations in SAS-COV-2
variants, such as 69/70 deletion, N501Y, and D614G. We used type-specific CISP NAs
(crNAs) to identify wild-type (crNA-W) and mutant (crNA-M) sequences of SAS-CoV-2. We successfully differentiated mutant variants from wild-type SAS-CoV-2 with a sensitivity of
10
−17 M (approximately 6 copies/μL). The assay took just 10 min with the Cas12a/crNA reaction
after a simple T-PC using a fluorescence reporting system. In addition, a sensitivity of 10
−16 M
could be achieved when lateral flow strips were used as readouts. The accuracy of T-CODS for
SAS-CoV-2 variant detection was 100 consistent with the sequencing data. In conclusion,
2
using the T-CODS platform, we accurately, sensitively, specifically, and rapidly detected
SAS-CoV-2 variants. This method may be used in clinical diagnosis'''}

request = requests.get(server_url + '/find_disease_names')
jsonData = json.loads(request.text)
diseases = jsonData['diseases']
print(diseases)