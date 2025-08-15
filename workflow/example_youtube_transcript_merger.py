import re
from task import Task, Binding, make_identity
from run import run_graph
from tasteful import delegator
from datetime import datetime
from functools import wraps


def current_time_human_readable():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def timer(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = current_time_human_readable()
        res = fn(*args, **kwargs)
        end = current_time_human_readable()
        print(f'{fn.__name__} started at {start} and ended at {end}')
        return res
    return wrapper


def make_llm_fn(prompt):
    def fn():
        print(f'Running prompt:{prompt}')
        print('-'*20)
        c = delegator.run(f'baris plain "{prompt}"')
        return c.out
    return fn



def clean_and_chunk_transcript(transcript):
    """
    Clean a transcript by removing timestamp markers like [00:00],
    but keep every 20th timestamp for reference.
    
    Args:
        transcript (str): The raw transcript text with timestamps
        
    Returns:
        str: Cleaned transcript with most timestamps removed
    """
    import re
    
    # Pattern to match timestamps like 00:00, 01:23, etc.
    timestamp_pattern = r'\d{2}:\d{2}'
    
    # Counter for timestamps
    count = 0
    
    # Function to process each match
    def replace_timestamp(match):
        nonlocal count
        count += 1
        
        # Keep every 20th timestamp
        if count % 20 == 0:
            return '<DIVIDER>'+match.group(0)+'</DIVIDER>'  # Return the original timestamp
        else:
            return ' '  # Remove the timestamp
    
    # Replace timestamps using the function
    cleaned_transcript = '<DIVIDER>00:00</DIVIDER>' + re.sub(timestamp_pattern, replace_timestamp, transcript)

    splitted = cleaned_transcript.split('<DIVIDER>')

    d = {}
    for chunk in splitted:
        if chunk.strip()=='':
            continue
        time, chunk_text = chunk.split('</DIVIDER>',1)
        d[time] = chunk_text
    
    return d

def merger(*args):
    return '\n\n'.join(args)

def clean_separate_and_improve_transcript(*args):
    """Clean, separate and improve a transcript"""
    # Clean the transcript
    # find occurances of [00:00] and replace with empty string, except the every 20th occurance
    
    raw_transcript = ''.join(args)
    
    print(f"Raw transcript: {raw_transcript}")
    chunks = clean_and_chunk_transcript(raw_transcript)
    
    tasks = []
    for k, v in chunks.items():
        improver = Task(
            make_llm_fn(
                f"""take the following transcripts from youtube. convert it to meaningful paragraphs by coherent meanings. 
            and also correct punctuations and issues in it. Clean it. Be careful, always be very very loyal to the original text
            
            Never ever omit the text from original text!!! This is very very important!

            Below is the text:
            ```
            {v}
            ```
            
            Always be very very loyal to the original text! Only output the cleaned and improved text! Say nothing else!"""
            ),
            ready=True,
            yielder=True,
        )
        cleaned_timestamp = re.sub(r'\W+', '_', k)
        improver.name = f"improver_{cleaned_timestamp}"
        tasks.append(improver)
        
    merger_task = Task(
        merger,
        fn_args=[Binding(improver) for improver in tasks],
        yielder=True,
    )
    tasks.append(merger_task)
    
    for res, task_name in run_graph(tasks):
        if task_name.startswith('improver'):
            print(f"Received partial result from {task_name.split(':')[0]}: {res}")
        else:
            print(f"Received final result from {task_name}: {res}")
        print('-'*20+'\n\n')


if __name__ == "__main__":
    clean_separate_and_improve_transcript(
        '''
0:03
for the thousands in attendance and the millions watching around the world ladies and gentlemen let's get ready to
0:11
pipe the he needs no introduction he's
0:23
the people's champion from Chicago Illinois presenting reinventing the
0:29
parser generator David thank thank you
0:42
very much where were you and I went up for tenure by the way all right all
0:49
right so we're gonna we're gonna talk about parser generators in here I also have to apologize kind of get head of
0:54
cold so if my voice kind of drops out and deal with that yeah parser generators well let's start
1:01
this off I think the one thing I would start with is that programming is basically magic if you think about it
1:07
and a big part of programming involves different levels of abstraction
1:13
basically you take problems and you try to you know figure out ways to solve problems and did you know involves
1:19
things like naming things and data structures and functions and and objects but at some point you're just going to
1:25
exhaust all the possibilities of that and you're gonna need to go further than objects or something right I mean it's
1:32
like we're like where do you go from where do you go from there you could jump into the land of Python magic
1:39
methods you know Python gives you great flexibility and sort of modifying the
1:45
the environment there so you could do you can do magic methods I don't know if
1:52
people get angry with all your magic methods you can deflect their anger by just calling all of those dunder methods
1:58
right so you know like mispronounce it then they're gonna be angry about that you can okay okay you do magic methods but you
2:06
might take it kind of a step further than that and get into it I guess what describes linguistic abstraction which
2:13
is basically making your own programming language your own language related to the problem that you're working on and
2:20
there's a lot of history of this I mean involving things like mathematical notation and programming languages and
2:25
things like sequel and config files and hardware description languages and all this all this stuff so you know there's
2:32
certain problems where that really you know like you try to make a language it's kind of match the problem and in
2:38
doing that you're trying to simplify the problem the the big problem is how do
2:43
you do that like I mean you know just as an example let's let's say I don't know you made your own programming language
2:50
and you had a statements like that how do you parse that like I mean if I were to ask you it could take that code and
2:56
like break it up and parse it and understand it that turns out to be a pretty non-trivial problem I mean this
3:02
is this is more than just sort of string splitting or string partitioning or something like that I mean there's
3:08
there's basically the problem of breaking that up into tokens so recognizing that you know a is an
3:15
identifier and you have numbers and symbols and so forth so there's kind of a tokenizing process there's also just
3:22
the problem of like recognizing so there's a grammar of this thing like like what is this code you know what is
3:29
it exactly and so there's there's kind of a notion of a grammar for what a program is you can say well you know
3:34
program is a bunch of statements and well what's statements well statements are like one like many statements
3:40
followed by one statement or a single statement and then you can ask what are the different statements I mean there's
3:45
there's like assignment there's printing there's expressions I mean suddenly this this turns into a sort of a very
3:51
non-trivial problem and then even if you kind of get past that you run into all
3:56
these problems of like look even if you could break all this this code apart what do you turn it into like what's
4:03
what's the end result of this thing and you might end up building things like
4:09
abstract syntax trees or other other things but it's it's it's a highly kind of non-trivial problem too
4:15
get into that if you ask you know co-workers or something you say well how
4:20
do I solve this problem one thing that they might direct you to is they would say we'll go read the Dragon book this
4:27
is the same it I modified it a little bit but you know they said that they
4:32
yeah that you know the infamous Dragon book this is something that you that you
4:37
give to students if you want to make them cry or something like like if you go in that book I mean the whole book
4:44
basically looks something like that I mean it's it's like very dense very mathematical
4:50
you know you'll walk away from that and just you know head spinning and the
4:56
truth of the matter is like basically for doing parsing most people turn to tools I mean this is you know this is a
5:03
well kind of trodden area of CS people have written you know tools to do parsing and tokenizing some of the sort
5:10
of more classic tools for this or Lex and yak on UNIX yak was developed in
5:15
kind of the early 1970s relax is kind of in the same ballpark and really kind of
5:21
the idea there is that they have you describe your language and kind of a higher level maybe something like this
5:29
where you'd write out your write out your grammar and then you run it through a code generator and then you get up
5:35
like a you get a bundle of C code or something and then you take that and compile it into your program now it's
5:44
not you know these are old tool turns out that Python works this way as well I mean this is maybe a little bit obscure
5:50
but if you go into the like the Python source code you'll find that it's parser
5:55
is basically automatically generated from a file I don't know their whether people have really seen that so I
6:02
thought I would just kind of like show you that real quick so this is the the C Python distribution here essentially if
6:09
you go into a directory there there's like a you know grammar directory you can find a file called grammar which is
6:15
like a high-level description of what Python syntax is if you if you look at
6:21
it let's just say just take a look at it there uh you all you know get this this thing saying okay well this is the
6:27
grammar for Python it's a little little description you know guide for how to change it and you'll find this you know kind of
6:35
description of what what the grammar is for Python and it goes on for a little little while there'll be quiz on reading
6:41
this later on but then what what happens with this is this grammar is
        '''
    )