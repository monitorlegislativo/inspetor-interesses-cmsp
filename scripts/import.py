import datastore.client
import csv, os
import md5

#Define elasticsearch database
url = "http://127.0.0.1:9200/inspetor/i"
client = datastore.client.DataStoreClient(url)

encoding = 'iso-8859-1'
def parse(fp):
    os.system("iconv -f "+ encoding + " -t utf-8 " + fp + " --output utf8-" + fp)
    fo = open("utf8-"+fp, 'rU')
    arquivo = csv.DictReader(fo, delimiter='#')
    parsed = []
    for linha in arquivo:
        parsed.append(linha)
    return parsed


os.chdir('raw')
projetos = parse('projetos.txt')
print 'Loaded projetos...'
autores = parse('autor.txt')
print 'Loaded autores...'
assuntos = parse('assunto.txt')
print 'Loaded assuntos...'
os.chdir('..')


def hex(id_projeto):
    return md5.new(id_projeto).hexdigest()

lista_projetos = {}
for p in projetos:
    id_projeto = p['TipoProj'] + '-' + p['NoProj'] + '-' + p['DataProj']
    projeto = p
    projeto['id'] = id_projeto
    projeto['autores'] = []
    projeto['assuntos'] = []
    lista_projetos[hex(id_projeto)] = projeto

autor_errors = 0
for a in autores:
    id_projeto = a['TipoProj'] + '-' + a['NoProj'] + '-' + a['DataProj']
    try:
        lista_projetos[hex(id_projeto)]['autores'].append(a['Autor'])
    except:
        #print 'Falha ao importar autores de ' + id_projeto
        autor_errors += 1

print 'Ocorreram ' + str(autor_errors) + ' erros na importacao dos autores'

assuntos_errors = 0
for a in assuntos:
    id_projeto = str(a['TipoProj']) + '-' + str(a['NoProj']) + '-' + str(a['DataProj'])
    try:
        lista_projetos[hex(id_projeto)]['assuntos'].append(a['Assunto'])
    except:
        #print 'Falha ao importar assuntos de ' + id_projeto
        assuntos_errors += 1

print 'Ocorreram ' + str(assuntos_errors) + ' erros na importacao dos assuntos'

def funkystuff(reader):
    for p in reader:
        yield p

print "Delete done"
print 'Mapping done'

client.upsert(funkystuff(projetos))
