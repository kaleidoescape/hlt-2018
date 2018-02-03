import os
import sys
import w2vconfig
import argparse

class AlterParser(argparse.ArgumentParser):
    """Change behaviour of ArgumentParser.error() to print help and exit."""
    def error(self, msg):
        sys.stderr.write('error: %s\n' % msg)
        self.print_help()
        sys.exit(2)

def parse_args():
    """Parse command line arguments."""
    parser = AlterParser(prog='evaluate.py', 
            description='Evaluate the performance of the translations from the model to a gold standard')
    parser.add_argument('--gold',
        type=str, 
        default=w2vconfig.dicts_dir + 'nl-ru.txt',
        help='file path to gold standard dictionary')
    parser.add_argument('--dictionary',
        type=str, 
        default=w2vconfig.dicts_dir + 'results.txt',
        help='file path to dictionary used for evaluation')
    args = parser.parse_args()
    return args


def load_dict(fp):
    d = set()
    with open(fp, 'r', encoding='utf-8') as infp:
        for line in infp:
            src_word, tar_word = line.split()
            if len(src_word) == 1 or len(tar_word) == 1:
                continue
            d.add((src_word, tar_word))
    return d
    
    
def evaluate(gold, result):
    count = 0
    for pair in result:
        if pair in gold:
            count += 1
    total_pairs = len(result)
    return (count / total_pairs) * 100
    
    
    
if __name__ == '__main__':
    args = parse_args()
    assert os.path.isfile(args.gold)
    assert os.path.isfile(args.dictionary)
    
    gold = load_dict(args.gold)
    result = load_dict(args.dictionary)
    
    accuracy = evaluate(gold, result)
    print("Accuracy on " + str(len(result)) + " word pairs: " + str(accuracy) + "%")
