from liblet import ANTLR, Tree, AnnotatedTreeWalker, Stack, show_calls
from parser import parse
import math
import random as rd
import operator as op
import functools as fs
from turtle import *
import sys
sys.tracebacklimit = 0

interpreter = AnnotatedTreeWalker('type')

#===and===
def _and(visit, ast):
    """
    Applica la short circuit evaluation sul numero di input.
    Scorre gl input da sinistra a destra e appena trova un valore `False`, blocca la valutazione e restituisce `False`.
    Altrimenti valuta tutti gli elementi e restituisce `True`.
    Effettua un controllo sui tipi. Restituisce un eccezione **TypeError** se i valori valutati non sono `Boolean`.
    """
    for child in ast.children:
        value = visit(child)
        if not isinstance(value, bool):
            raise TypeError("Gli input dei connettivi logici devono essere dei boolean")
        if not value:
            return False
    return True

#===or===
def _or(visit, ast):
    """
    Applica la short circuit evaluation sul numero di input.
    Scorre gl input da sinistra a destra e appena trova un valore `True`, blocca la valutazione e restituisce `True`.
    Altrimenti valuta tutti gli elementi e restituisce `False`.
    Effettua un controllo sui tipi. Restituisce un eccezione **TypeError** se i valori valutati non sono `Boolean`.
    """
    for child in ast.children:
        value = visit(child)
        if not isinstance(value, bool):
            raise TypeError("Gli input dei connettivi logici devono essere dei boolean")
        if value:
            return True
    return False

#===not===
def _not(visit, ast):
    """
    Applica l'operatore logico `not` all'valore in ingresso.
    Effettua un controllo sui tipi. Restituisce un eccezione **TypeError** se i valori valutati non sono `Boolean`.
    """
    value = visit(ast.children[0])
    if not isinstance(value, bool):
        raise TypeError("Gli input dei connettivi logici devono essere dei boolean")
    return not value

#===random===
def random(listParams):
    """
    Controlla il numero di parametri in ingresso.
    Se e' uno solo lo utilizza come limite massimo.
    Se sono due li utilizza come numero minimo e numero massimo tra i quali generare il numero random.
    """
    if len(listParams) == 1 :
        return rd.randrange(listParams[0])
    else:
        return rd.randint(listParams[0], listParams[1])

#===rerandom===
def rerandom(listParams):
    """
    Rende riproducibili i numeri randomici nell'esecuzione multipla del programma.
    Se non viene passato nessun seed viene usato uno di default che è 0.
    Altrimenti viene usato il seed indicato come parametro.
    """
    if len(listParams) == 0:
        rd.seed(0)
    else:
        rd.seed(listParams[0])

#===quotient===
def quotient(listParams):
    """
    Restituisce il quoziente dei due numeri che sono passati come parametri.
    Se il numero calcolato è intero restituisce un `int` altrimenti un `float`.
    Se il parametro è solo uno restituisce il reciproco.
    """
    if len(listParams) == 1:
        return 1/listParams[0]
    else:
        res = fs.reduce(op.truediv, listParams)
        return int(res) if res.is_integer() else res

#=== fixed quotient ===
def fixedQuotient(x,y):
    """
    Operatore di divisione insfisso.
    Applica la divisione tra i due numeri, effettua un controllo sul risultato:
    se e' un `INT` restituisce un `INT`, viceversa se e' `FLOAT` restituira' `FLOAT`
    """
    result = x/y
    return int(result) if result.is_integer() else result

#===arctan===
def arctan(listParams):
    """
    Calcola il valore dell'arcotangente in base al numero di parametri passati in ingresso
    """
    if len(listParams) == 1:
        math.degrees(math.atan(listParams[0]))
    else:
        math.degrees(math.atan2(listParams[1], listParams[0]))

#===radarctan===
def radarctan(listParams):
    """
    Calcola il valore dell'arcotangente in radianti in base al numero di parametri passati in ingresso
    """
    if len(listParams) == 1:
        math.atan(listParams[0])
    else:
        math.atan2(listParams[1], listParams[0])
    
#===set pen color===
def setPenColor(listParams):
    """
    Comando grafico che applica il cambio colore della tartaruga in base al set **RGB** passato come input.
    """
    if not all(isinstance(ele, (int, float)) for ele in listParams):
        raise TypeError("I parametri di un comando graphics devono essere tutti dei numeri")
    
    colormode(255)
    pencolor(listParams[0], listParams[1], listParams[2])

"""
Disppatch table contenente le funzioni riguardanti operazioni aritmetico-logice
"""
DT_OPERATORS = {
    '+':             lambda x, y: x + y,
    '-':             lambda x, y: x - y,
    '*':             lambda x, y: x * y,
    '/':             fixedQuotient,
    'sum':           lambda x: fs.reduce(op.add, x),
    'difference':    lambda x: fs.reduce(op.sub, x),
    'product':       lambda x: fs.reduce(op.mul, x),
    'quotient':      quotient,
    'arctan':        arctan,
    'radarctan':     radarctan,
    'lessp':         lambda x, y: x < y,
    'greaterp':      lambda x, y: x > y,
    'lessequalp':    lambda x, y: x <= y,
    'greaterequalp': lambda x, y: x >= y,
    '>':             lambda x, y: x > y,
    '<':             lambda x, y: x < y,
    '>=':            lambda x, y: x >= y,
    '<=':            lambda x, y: x <= y,
    '=':             lambda x, y: x == y,
    'remainder':     lambda x: math.remainder(x[0], x[1]),
    'modulo':        lambda x: x[0]%x[1],
    'power':         lambda x: x[0]**x[1],
    'int':           lambda x: int(x[0]),
    'round':         lambda x: round(x[0]),
    'sqrt':          lambda x: math.sqrt(x[0]),
    'exp':           lambda x: math.exp(x[0]),
    'log10':         lambda x: math.log10(x[0]),
    'ln':            lambda x: math.log(x[0]),
    'sin':           lambda x: math.degrees(math.sin(x[0])),
    'radsin':        lambda x: math.sin(x[0]),
    'cos':           lambda x: math.degrees(math.cos(x[0])),
    'radcos':        lambda x: math.cos(x[0]),
    'random':        random,
    'rerandom':      rerandom,
    'not':           _not,
    'and':           _and,
    'or':            _or,
    'minus':         lambda x: -(x[0])
}

"""
Dispatch table contenente tutte le operazioni di tipo grafico, e'stata utilizzata la libreria **turtle**
"""
DT_GRAPHICS = {
    'rw':           lambda: input(),
   	'fd':           lambda x: forward(x[0]),
   	'bk':           lambda x: bk(x[0]),
   	'rt':           lambda x: rt(x[0]),
   	'lt':           lambda x: lt(x[0]),
   	'setxy':        lambda x: setpos(x[0], x[1]),
   	'setpos':       lambda x: setpos(x[0]),
   	'setx':         lambda x: setx(x[0]),
   	'sety':         lambda x: sety(x[0]),
   	'seth':         lambda x: seth(x[0]),
   	'arc':          lambda x: circle(x[0], x[1]),
   	'setpc':        setPenColor,
   	'setpensize':   lambda x: pensize(x[0]),
   	'cs':           clear,
   	'pu':           pu,
   	'pd':           pd,
   	'ht':           ht,
   	'st':           st,
   	'home':         home,
   	'clean':        clear
}

#===zero parameters functions===
def zeroPrarameterFunctions(visit, ast):
    """
    Viene richiamata da **graphics** definita in [[interpreter.py#graphic]].
    Tramite il nome del nodo accede alla dispatch table ed esegue la funzione selezionata non passando nessun parametro alla funzione chiamata.
    """
    DT_GRAPHICS[ast.root['name']]

#===more parameter functions===
def morePrarameterFunctions(visit, ast):
    """
    Viene richiamata da **graphics** definita in [[interpreter.py#graphic]].
    Tramite il nome del nodo accede alla dispatch table ed esegue la funzione selezionata.
    Passa come parametri alla funzione un array contente i risultati della visita ricorsiva di tutti i figli del nodo.
    """
    params = []
    if ast.children[0].root['type'] == 'block':
        params = visit(ast.children[0])
    else:
        params = [visit(child) for child in ast.children]

    if not all(isinstance(ele, (int, float)) for ele in params):
        raise TypeError("In un espressione gli operandi devono essere int o float")
    DT_GRAPHICS[ast.root['name']](params)

#===operations===
def operations(visit, ast):
    """
    Viene richiamata da **exceptions** definita in [[interpreter.py#expression]].
    Visita ricorsivamente tutti i figli dispari per prendere tutti i segni dell'espressione.
    Visita ricorsivamente tutti i figli pari per prendere tutti i valori numerici dell'espressione.
    Iterazione per iterazione applico all'accumulatore e al numero l'operazione e restituisco l'accumulatore.
    Controllo che tutti i tipi all'interno di numbers siano umerici altrimenti lancio un' eccezione **TypeError**
    """
    
    numbers = [visit(child) for child in ast.children[::2]]

    if not all(not isinstance(ele, bool) and isinstance(ele, (int, float)) for ele in numbers):
        raise TypeError("In un espressione gli operandi devono essere int o float")
    
    signs = [visit(child) for child in ast.children[1::2]]

    acc = numbers[0]
    signIndex = 0
    for number in numbers[1:]:
        acc = DT_OPERATORS[signs[signIndex]](acc, number)
        signIndex += 1
    
    return acc

#===prog===
@interpreter.register
def prog(visit, ast):
    """
    Non esegue alcuna operazione, visita ricorsivamente tutti i suoi figli.
    """
    for child in ast.children: visit(child)

#===line===
@interpreter.register
def line(visit, ast):
    """
    Non esegue alcuna operazione, visita ricorsivamente tutti i suoi figli.
    """
    for child in ast.children:
        visit(child)

#===expression===
@interpreter.register
def expression(visit, ast):
    """
    Se ha un unico figlio restituisce il valore della chiamata ricorsiva su quest'ultimo.
    Altrimenti restituisce il valore della chiamata della funzione **operations**.
    Se presente applica al risultato il segno dell'espressione
    """
    result = None

    if len(ast.children) == 1:
        result = visit(ast.children[0])
    else:    
        result = operations(visit, ast)

    if 'sign' in ast.root:
        return int(ast.root['sign']+str(1))*result
    else:
        return result

#===operators===
@interpreter.register
def Op(visit, ast):
    """
    Restituisce il valore dell'operatore.
    I possibili operatori sono:

    `[+, -, *, /]`
    """
    return ast.root['value']

#===comparison operator===
@interpreter.register
def comparisonOperator(visit, ast):
    """
    Restituisce il valore dell'operatore.
    I possibili operatori sono:

    `[<, >, =, >=, <=]`
    """
    return ast.root['value']

#===print===
@interpreter.register
def pr(visit, ast):
    """
    Stampa il valore della visita ricorsiva dei figli.
    """
    
    for child in ast.children:
        print(visit(child))

#===arithmetic and boolean operations===
@interpreter.register
def arithmBoolOperations(visit, ast):
    """
    Gestisce tutti i tipi di operazioni aritmetiche e logiche tramite la dispatch table `DT_TABLE`.
    Effettua un controllo sui tipi delle operazioni aritmetiche, se non sono numeri lancia un eccezione di tipo **TypeError**.
    """
    if ast.root['name'] in ['and', 'or', 'not']:
        return DT_OPERATORS[ast.root['name']](visit, ast)

    params = [visit(child) for child in ast.children]
    if not all(not isinstance(ele, bool) and isinstance(ele, (int, float)) for ele in params):
        raise TypeError("In un espressione gli operandi devono essere int o float")

    return DT_OPERATORS[ast.root['name']](params)

#===make===
@interpreter.register
def make(visit, ast):
    """
    Salva nel activation record corrente il una coppia con chiave il nome della variabile contenuto 
    nel primo figlio e come valore il valore della variabile contenuto nel secondo figlio.
    Controllo che il nome della variabile sia una stringa altrimenti lancio
    un eccezione di tipo **TypeError**
    """
    memory = interpreter.GLOBAL_MEMORY
    name = visit(ast.children[0])
    value = visit(ast.children[1])

    if not isinstance(name, str):
        raise ValueError("Il nome di una variabile deve essere una stringa")
    if value == None:
        raise TypeError("Non posso assegnare ad una variabile un valore nullo")

    memory[visit(ast.children[0])] = value

#===deref===
@interpreter.register
def deref(visit, ast):
    """
    Cerca all interno dell'activation record corrente il nome della variabile di cui si vuole conosce il valore, 
    e lo restituisce se presente, altrimenti cerca nella GLOBEL_MEMORY, se il valore non e' presente neanche li,
    lancia un eccezzione di tipo **NameError**.
    Se e' un numero controlla che ci sia il segno e lo aggiunge al numero che restituisce.
    """

    memory_stack = interpreter.ACTIVATION_RECORDS.peek()
    memory_global = interpreter.GLOBAL_MEMORY
    name = visit(ast.children[0])
    res=''

    if name in memory_stack:
        res = memory_stack[name]
    elif name in memory_global:
        res = memory_global[name]
    else:
        raise NameError("La variabile " + name + " non è stata dichiarata")
    
    if not isinstance(res, str) and 'sign' in ast.root:
        return int(ast.root['sign']+"1")*res
    return res   



#===graphic operations===
@interpreter.register
def graphic(visit, ast):
    """
    Esegue due tipi di funzioni diverse in base al numero di parametri che richiedono:

        - `zeroPrarameterFunctions` 
        - `morePrarameterFunctions` 

    Le operazioni svolta da questa funzione sono di tipo grafico, ed e' utilizzata la libreria **turtle**
    """
    if (len(ast.children) == 0):
        return zeroPrarameterFunctions(visit, ast)
    else:
        return morePrarameterFunctions(visit, ast)

#===if===
@interpreter.register
def ifState(visit, ast):
    """
    Esegue il blocco dell if contenuto nel secondo figlio del nodo, se la condizione contenuta nel primo figlio e' verificata.
    Effettuo un controllo sul fatto che la condizione sia di tipo boolean, altrimenti lancio un eccezzione di tipo **TypeError**
    """
    result = []
    condition = visit(ast.children[0])

    if not isinstance(condition, bool):
        raise TypeError("La condizione di un IF deve essere un boolean")

    if condition:
        return visit(ast.children[1])

#===if else===
@interpreter.register
def ifelseState(visit, ast):
    """
    Esegue il blocco contenuto nel secondo figlio del nodo se la condizione contenuta 
    nel primo figlio e' verificata altrimenti esegue il blocco dell'else contenuto nel terzo figlio.
    Effettuo un controllo sul fatto che la condizione sia di tipo boolean, altrimenti lancio un eccezzione di tipo **TypeError**
    """
    result = []
    condition = visit(ast.children[0])

    if not isinstance(condition, bool):
        raise TypeError("La condizione di un IF deve essere un boolean")

    if condition:
        return visit(ast.children[1])
    else:
        return visit(ast.children[2])

#===repeat===
@interpreter.register
def repeatState(visit, ast):
    """
    Esegue il blocco contenuto nel secondo figlio per un numero di volte che e' specificato nel primo figlio del nodo.
    Controlla ogni ciclo se e' stata effettuata un operazione di `output`oppure `stop` se cosi fosse interrompe il ciclo.
    Effettua un controllo sul tipo del parametro di repeat, se non è un int lancia un eccezione di tipo **TypeError**
    """
    memory = interpreter.ACTIVATION_RECORDS.peek()
    value = visit(ast.children[0])

    if not isinstance(value, int):
        raise TypeError("REPEAT deve avere un int come parametro")

    for _ in range(value):
        if 'retval' in memory or 'stop' in memory:
            return
        visit(ast.children[1])

#===while===
@interpreter.register
def whileState(visit, ast):
    """
    Esegue il blocco contenuto nel secondo figlio finche la condizione specificata nel primo figlio del nodo non si falsifica.
    Controlla ogni ciclo se e' stata effettuata un operazione di `output`oppure `stop` se cosi fosse interrompe il ciclo.
    Effettuo un controllo sul fatto che la condizione sia di tipo boolean, altrimenti lancio un eccezzione di tipo **TypeError**
    """
    memory = interpreter.ACTIVATION_RECORDS.peek()

    while visit(ast.children[0]):
        if 'retval' in memory or 'stop' in memory:
            return
        visit(ast.children[1])

#===procedure declaration===
@interpreter.register
def procedureDeclaration(visit, ast):
    """
    Salva il sottoalbero della funzione all interno del dizionario `FUNCTIONS` e come chiave il nome della funzione.
    Modifica il nome del tipo del nodo cosi che quanto verra richiamata la funzione e quindi interpretata, possa essere fatto cio' tramite un apposita funzione.
    """
    ast.root['type'] = 'procedureExec'
    interpreter.FUNCTIONS[ast.root['name']] = ast

#===procedure execution===
@interpreter.register
def procedureExec(visit, ast):
    """
    Interpreta la funzione.
    """
    memory = interpreter.ACTIVATION_RECORDS.peek()
    for child in ast.children:
        if 'retval' in memory or 'stop' in memory:
            return
        visit(child)

#===procedure invocation===
@interpreter.register
def procedureInvocation(visit, ast):
    """
    Cerca la funzione all'interno di `FUNCTIONS`.
    Aggiunge un nuovo activation record allo stack, esegue la funzione, fa il pop del record nello stack.
    Come ultima cosa restituisce il valore della funzione.
    """
    name = ast.root['name']
    if name in interpreter.FUNCTIONS:
        function = interpreter.FUNCTIONS[name]
    else:
        raise NameError("La funzione non è stata dichiarata")
    
    paramsName = function.root['params']
    paramsValue = [visit(child) for child in ast.children]

    if len(paramsName) != len(paramsValue):
        raise TypeError("Numero di parametri per la funzione `" +  name + "` non corretto")
    
    interpreter.ACTIVATION_RECORDS.push(dict(zip(paramsName, paramsValue)))
    visit(function)

    memory = interpreter.ACTIVATION_RECORDS.peek()

    if 'retval' in memory:
        return interpreter.ACTIVATION_RECORDS.pop()['retval']
    interpreter.ACTIVATION_RECORDS.pop()

#===output===
@interpreter.register
def opState(visit, ast):
    """
    Simula il ritorno con valore di una funzione.
    Salva nello stack con il nome di `retval` il valore della chiamata ricorsiva sul primo figlio.
    """
    if len(interpreter.ACTIVATION_RECORDS) == 1:
        raise SyntaxError("Non si può avere un output state al di fuori di una funzione")
    
    memory = interpreter.ACTIVATION_RECORDS.peek()
    memory['retval'] = visit(ast.children[0])

#===stop===
@interpreter.register
def stopState(vist, ast):
    """
    Simula il ritorno senza valore di una funzione.
    Salva nello stack con il nome di `retval` il valore `None`.
    """
    if len(interpreter.ACTIVATION_RECORDS) == 1:
        raise SyntaxError("Non si può avere uno stop state al di fuori di una funzione")

    memory = interpreter.ACTIVATION_RECORDS.peek()
    memory['stop'] = None

#===block===
@interpreter.register
def block(visit, ast):
    """
    Visita ricorsivamente tutti i figli del nodo e restituisce con risultato una lista contenente i valori di ritorno
    delle sole funzioni che restituiscono effettivamente qualcosa.
    """
    memory = interpreter.ACTIVATION_RECORDS.peek()
    result = []
    for child in ast.children:
        if 'retval' in memory or 'stop' in memory:
            return
        result.append(visit(child))

    result = [ele for ele in result if ele != None]
    if (len(result) != 0):
        return result[-1]
    
#===read word===
@interpreter.register
def rw(visit, ast):
    """
    Aspetta un input da tastiera e lo restituisce.
    Se l'input è un numero lo converte in numero.
    """

    value = input()

    try:
        return int(value) if float(value).is_integer() else float(value)
    except ValueError:
        return str(value)

@interpreter.register
def Boolean_(visit, ast):
    return ast.root['value']

@interpreter.register
def STRINGLITERAL(visit, ast):
    return str(ast.root['value'])

@interpreter.register
def STRING(visit, ast):
    return str(ast.root['value'].replace('"', ''))

@interpreter.register
def FLOAT(visit, ast):
    if 'sign' in ast.root:
        return float(ast.root['sign'] + str(ast.root['value']))
    return float(ast.root['value'])

@interpreter.register
def INT(visit, ast):
    if 'sign' in ast.root:
        return int(ast.root['sign'] + str(ast.root['value']))
    return int(ast.root['value'])

#===run===
def run(code):
    """
    Inizializza un nuovo spazio di memoria per i nomi di funzioni e uno stack vuoto.
    Interpreta il codice datogli in ingresso, e restituisce il risultato se presente.
    """
    interpreter.FUNCTIONS = {}
    interpreter.ACTIVATION_RECORDS = Stack([{}])
    interpreter.GLOBAL_MEMORY = {}
    interpreter(parse(code))
    try:
        bye()
    except Terminator:
        pass
