from liblet import ANTLR, Tree, AnnotatedTreeWalker
import os

class UndefinedNodeException(Exception):
    pass

with open('logoGrammar.g4') as inf:
        grammar = inf.read()

ANTLR_GRAMMAR = ANTLR(grammar)
logoToAst = AnnotatedTreeWalker('name')

"""
Dispatch table che viene usata per standardizzare i nomi dei comandi che hanno anche un abbreviazione.
"""
DT_COMMAND = {
    'print': 'pr',
    'forward': 'fd',
    'back': 'bk',
    'left': 'lt',
    'right': 'rt',
    'setheading': 'seth',
    'showturtle': 'st',
    'hideturtle': 'ht',
    'clearscreen': 'cs',
    'setpencolor': 'setpc',
    'penup': 'pu',
    'pendown': 'pd',
    'output': 'op',
    'less?': 'lessp',
    'greater?': 'greaterp',
    'lessequal?': 'lessequalp',
    'greaterequal?': 'greaterequalp',
    'and': 'and',
    'or': 'or',
    'not': 'not'
}

def children_filter(key,filter_elem, children):
    return list(filter(lambda child: child.root[key] not in filter_elem, children))

OPERATORSNAME_TYPE = 'Op'
NAME_TYPE = 'STRING'
ARBOOLOPERATIONS_TYPE = 'arithmBoolOperations'

#===prog===
@logoToAst.register
def prog(visit, tree):
    """
    Rappresenta il nodo iniziale dell'albero di parsing.
    Ogni figlio rappresenta una linea del programma
    La funzione ripulisce da tutti i nodi non necessari e restituisce l'albero che ha per figli la visita ricorsiva di ognuno di essi.
    """
    return Tree({'type': tree.root['name']}, [visit(child) for child in tree.children if child.root["name"] != "EOL"])

#===line===
@logoToAst.register
def line(visit, tree):
    """
    Ogni figlio di line rappresenta una linea del programma.
    Una line può contenere più espressioni o comandi e sono reppresentati dai figli.
    """
    return Tree({'type': tree.root['name']},[visit(child) for child in tree.children])

# ===arithmetic and boolean operations===
@logoToAst.register
def arithmBoolOperations(visit, tree):
    """
    Definisce tutte le operazioni di tipo aritmetico e booleano.
    Standardizza i nomi scrivendoli tutti in minuscolo e se peresentano abbreviazioni viene usato il nome all interno 
    della dispatch table.
    Ogni figlio dell'albero rappresenta un parametro dell'operazione.
    """
    child = tree.children[0]

    children = children_filter('name', ['(',')','EOL'], child.children)

    name = DT_COMMAND.get(children[0].root['name'].lower()) if children[0].root['name'].lower() in DT_COMMAND.keys() else children[0].root['name'].lower()

    return Tree({'type': tree.root['name'], 'name': name}, [visit(child) for child in children[1:]])

#===control structure===
@logoToAst.register
def controlStructure(visit, tree):
    """
    Definisce tutte le strutture di controllo.
    I nomi delle strutture di controllo che hanno delle abbreviazioni vengono standardizzati tramite la dispatch table.
    Al nome di ognuna di essi viene agginta la parola **State** per non creare conflitto con python.
    L'albero è definito in base al comando.
    """
    child = tree.children[0]
    children = children_filter('name', ['(',')', 'EOL'], child.children)

    name = DT_COMMAND.get(children[0].root['name'].lower()) if children[0].root['name'].lower() in DT_COMMAND.keys() else children[0].root['name'].lower()

    return Tree({'type': name+"State"}, [visit(child) for child in children[1:]])

#===graphic===
@logoToAst.register
def graphic(visit, tree):
    """
    Definisce tutte i comandi di tipo grafico.
    Vengono eliminate le parentesi se sono presenti.
    Ogni figlio rappresenta un parametro del comando, un nodo può anche non avere nessun figli.
    """
    child = tree.children[0]
    children = children_filter('name', ['EOL'], child.children)

    name = DT_COMMAND.get(children[0].root['name'].lower()) if children[0].root['name'].lower() in DT_COMMAND.keys() else children[0].root['name'].lower()

    return Tree({'type': tree.root['name'], 'name': name}, [visit(child) for child in children[1:]])

#===sys===
@logoToAst.register
def sys(visit, tree):
    """
    Definisce le funzioni print e make.
    Standardizza i nomi tramite la dispatch table definita in [[parser.py#command]]
    I figli definiscono i parametri dei comandi.
    """
    child = tree.children[0]

    children = children_filter('name', ['(',')','EOL'], child.children)

    name = DT_COMMAND.get(children[0].root['name'].lower()) if children[0].root['name'].lower() in DT_COMMAND.keys() else children[0].root['name'].lower()

    return Tree({'type': name}, [visit(child) for child in children[1:]])
    
#===expression===
@logoToAst.register
def expression(visit, tree):
    """
    Rappresenta un espressione la quale a sua volta può essere composta da:

        - Numeri 
        - Deref
        - Invocazioni di procedura
        - Strutture di controllo
        - String literal
        - Boolean
        - Connettivi logici

    Possono essere fatte delle operazioni tra espressioni che sono:
    
        - Somma
        - Sottrazione
        - Moltiplicazione
        - Divisione
        - Confronto

    L'espressione rappresenta in sostanza tutto cio' che restituisce un risultato.
    Non tutte le operazioni tra i componenti delle espressioni sono lecite.
    Sono presenti controlli a tal proposito che lanciano un eccezione di **TypeError** se vengono fatte
    operazioni non permesse tra i vari tipi.
    """
    sign = []
    children = children_filter('name',['(',')', 'EOL'], tree.children)

    for child in children:
        if child.root['name'] in ['+', '-']: 
            sign.append(child.root['name'])
        else: break

    if len(sign) != 0: 
        if sign.count('-') % 2 != 0:
            sign = '-'
        else:
            sign = '+'

        return Tree({'type': tree.root['name'], 'sign': sign}, [visit(child) for child in children if child.root['name'] not in ['+', '-']])


    return Tree({'type': tree.root['name']}, [visit(child) for child in children])

#===number===
@logoToAst.register
def number(visit, tree):
    """
    Nodo che rappresenta un valore numerico che puo' essere o `INT` oppure `FLOAT`.
    Non ha nessun figlio.
    """
    return Tree({'type': tree.children[0].root['name'], 'value': tree.children[0].root['value']})

#===muldivOperator
@logoToAst.register
def muldivoperators(visit, tree): 
    """
    Rappresenta gli operatori di **moltipolicazione** e **divisione**.
    Non ha nessun figlio.
    """
    return Tree({'type': OPERATORSNAME_TYPE, 'value': tree.children[0].root['value']})


#===addSubOperator
@logoToAst.register
def addsuboperators(visit, tree):
    """
    Rappresenta gli operatori di **somma** e **sottrazione**.
    Non ha nessun figlio.
    """
    return Tree({'type': OPERATORSNAME_TYPE, 'value': tree.children[0].root['value']})

#===stringliteral===
@logoToAst.register
def STRINGLITERAL(visit, tree):
    """
    Rappresenta una stringa.
    Il valore all interno del nodo viene salvato senza il carattere `"`
    """
    return Tree({'type': tree.root['name'], 'value': tree.root['value'].replace('"', '')})

#===value===
@logoToAst.register
def value(visit, tree):
    """
    Il nodo value non viene considerato, viene saltato e restituisce la visita ricorsiva sul suo unico figlio
    """
    return visit(tree.children[0])


#===procedureDeclaration===
@logoToAst.register
def procedureDeclaration(visit, tree):
    """
    Rappresenta una dichiarazione di funzione.
    Come campo del nodo c'è un array con i nomi dei parametri.
    I figli invece rappresentano il corpo della funzione.
    """
    children = children_filter('name', ['EOL'], tree.children)
    children = [visit(child) for child in children[1:-1]]
    name = children[0].root['value']
    params = [child.root['value'] for child in children if child.root['type'] == 'parameterDeclarations']
    return Tree({'type': tree.root['name'], 'name': name, 'params': params}, [child for child in children if child.root['type'] != 'parameterDeclarations'])

#===parameterDeclaration===
@logoToAst.register
def parameterDeclarations(visit, tree):
    """
    Rappresenta la dichiarazione dei parametri della funzione
    """
    return Tree({'type': tree.root['name'], 'value': visit(tree.children[1]).root['value']})
    
#===procedureInvocation===
@logoToAst.register
def procedureInvocation(visit, tree):
    """
    Rappresenta un invocazione di procedura.
    I figli rappresentano i parametri.
    """
    children = children_filter('name', ['(',')', 'EOL'], tree.children)

    return Tree({'type': tree.root['name'], 'name': children[0].children[0].root['value']}, [visit(child) for child in children[1:]])

#===parameters===
@logoToAst.register
def parameters(visit, tree):
    """
    Rappresenta i parametri di un invocazione di funzione.
    Presenta un unico figlio che è il parametro effettivo.
    """
    return visit(tree.children[0])

#===block===
@logoToAst.register
def block(visit, tree):
    """
    Definisce un blocco di istruzioni.
    Ogni figlio del blocco rappresenta un istruzione.
    """
    return Tree({'type': tree.root['name']}, [visit(child) for child in tree.children[1:-1] if child.root['name'] != 'EOL'])

#===comparison===
@logoToAst.register
def comparison(visit, tree):
    """
    Definisce l'operazione di comparazione tra due valori comparabili.
    Vengono eliminatei i nodi rappresentanti le parentesi se presenti.
    Contiene tre figli i quali rappresentano l'operazione e i due operandi.
    """
    children = children_filter('name', ['(',')','EOL'], tree.children)

    return Tree({'type': tree.root['name']}, [visit(child) for child in children])

#===comparisonOperator===
@logoToAst.register
def comparisonOperator(visit, tree):
    """
    Definisce gli operatori booleani di comparazione `[>, <, =, >=, <=]`
    """
    return Tree({'type': tree.root['name'], 'value': tree.children[0].root['name']})

#===boolean===
@logoToAst.register
def Boolean_(visit, tree):
    """
    Rappresenta un boolean. 
    Siccome i valori `True` e `False` non sono case sensitive e possono presentare un carattere `"` prima del nome
    standardizzo i nomi e li salvo all'interno del nodo.
    """
    value = tree.root['value'].replace('"', '').lower()
    if (value == 'false'):
        return Tree({'type': tree.root['name'], 'value': False})
    else:
        return Tree({'type': tree.root['name'], 'value': True})

#===deref===
@logoToAst.register
def deref(visit, tree):
    """
    Definisce la deferenziazione di una variabile.
    Il nodo padre ha sempre un figlio che rappresenta il nome della variabile da referenziare
    """
    if (tree.children[0].root['name'] == ':'):
        return Tree({'type': tree.root['name']}, [visit(tree.children[1].children[0])])
    
    return Tree({'type': tree.root['name']}, [visit(tree.children[1])])

#===readword===
@logoToAst.register
def rw(visit, tree):
    """
    Definisce il nome dell procedure Read Word
    """
    return Tree({'type': tree.root['name']})

@logoToAst.register
def name(visit, tree):
    return Tree({'type': NAME_TYPE, 'value': tree.children[0].root['value']})

#===and===
@logoToAst.register
def and_(visit, tree):
    """
    Rappresenta l'operazione logica di and, i figli rappresentano i parametri dell'istruzione.
    Come figli possono esserci anche dei blocchi di istruzioni logiche.
    """
    children = children_filter('name', ['(',')', 'EOL'], tree.children)
    
    return Tree({'type': ARBOOLOPERATIONS_TYPE, 'name': DT_COMMAND.get(children[0].root['name'].lower())}, [visit(child) for child in children[1:]])

#===or===
@logoToAst.register
def or_(visit, tree):
    """
    Rappresenta l'operazione logica di or, i figli rappresentano i parametri dell'istruzione.
    Come figli possono esserci anche dei blocchi di istruzioni logiche.
    """
    children = children_filter('name', ['(',')', 'EOL'],tree.children)
    
    return Tree({'type': ARBOOLOPERATIONS_TYPE, 'name': DT_COMMAND.get(children[0].root['name'].lower())}, [visit(child) for child in children[1:]])

#===not===
@logoToAst.register
def not_(visit, tree):
    """
    Rappresenta l'operazione logica di and, il figlo rappresenta il parametro dell'istruzione.
    """
    children = tree.children
    return Tree({'type': ARBOOLOPERATIONS_TYPE, 'name': DT_COMMAND.get(children[0].root['name'].lower())}, [visit(child) for child in children[1:]])

#===string===
@logoToAst.register
def STRING(visit, tree):
    """
    Definisce una stringa, il valore viene salvato all'interno del nodo senza il carattere `"`
    """
    return Tree({'type': tree.root['name'], 'value': tree.root['value'].replace('"', '')})

#===parse===
def parse(code):
    """
    La funzione prende in input il codice **logo** da parsare, e ristruttura l'albero di parsing generato da ANTLR che restituira' come output.
    """
    try:
        return logoToAst(ANTLR_GRAMMAR.tree(code, 'prog'))
    except Exception:
        print("---Errore di parsing---")
