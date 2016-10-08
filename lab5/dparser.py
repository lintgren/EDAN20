"""
Gold standard parser
"""
__author__ = "Pierre Nugues"

import transition
import conll
import features



def reference(stack, queue, state):
    """
    Gold standard parsing
    Produces a sequence of transitions from a manually-annotated corpus:
    sh, re, ra.deprel, la.deprel
    :param stack: The stack
    :param queue: The input list
    :param state: The set of relations already parsed
    :return: the transition and the grammatical function (deprel) in the
    form of transition.deprel
    """


    # Right arc

    if stack and stack[0]['id'] == queue[0]['head']:
        # print('ra', queue[0]['deprel'], stack[0]['cpostag'], queue[0]['cpostag'])
        deprel = '.' + queue[0]['deprel']
        stack, queue, state = transition.right_arc(stack, queue, state)
        return stack, queue, state, 'ra' + deprel
    # Left arc
    if stack and queue[0]['id'] == stack[0]['head']:
        # print('la', stack[0]['deprel'], stack[0]['cpostag'], queue[0]['cpostag'])
        deprel = '.' + stack[0]['deprel']
        stack, queue, state = transition.left_arc(stack, queue, state)
        return stack, queue, state, 'la' + deprel
    # Reduce
    if stack and transition.can_reduce(stack, state):
        for word in stack:
            if (word['id'] == queue[0]['head'] or
                        word['head'] == queue[0]['id']):
                # print('re', stack[0]['cpostag'], queue[0]['cpostag'])
                stack, queue, state = transition.reduce(stack, queue, state)
                return stack, queue, state, 're'
    # Shift
    # print('sh', [], queue[0]['cpostag'])
    stack, queue, state = transition.shift(stack, queue, state)
    return stack, queue, state, 'sh'


if __name__ == '__main__':
    train_file = 'swedish_talbanken05_train.conll'
    test_file = 'swedish_talbanken05_test_blind.conll'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']
    feature_names = [ 'word_s0', 'pos_s0','word_s1', 'pos_s1','word_q0', 'pos_q0', 'word_q1', 'pos_q1','can_re','can_ra']
    feature_names2 = ['word_s0', 'pos_s0', 'word_s1', 'pos_s1', 'word_q0', 'pos_q0', 'word_q1', 'pos_q1', 'can_re',
                     'can_ra','pos_n1','word_n1','word_lefts','word_rights']

    sentences = conll.read_sentences(train_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006)

    sent_cnt = 0
    X = list()
    Y = list()
    for sentence in formatted_corpus:
        sent_cnt += 1
        if sent_cnt % 1000 == 0:
            print(sent_cnt, 'sentences on', len(formatted_corpus), flush=True)
        stack = []
        queue = list(sentence)
        state = {}
        state['heads'] = {}
        state['heads']['0'] = '0'
        state['deprels'] = {}
        state['deprels']['0'] = 'ROOT'
        transitions = []
        #features.extract(stack,queue,state,feature_names,sentence)
        #if sent_cnt<2:
        while queue:
                X.append(features.extract2(stack,queue,state,feature_names2,sentence))
                stack, queue, state, trans = reference(stack, queue, state)
                transitions.append(trans)
                Y.append(trans)
        stack, state = transition.empty_stack(stack, state)
        #print('Equal graphs:', transition.equal_graphs(sentence, state))

        # Poorman's projectivization to have well-formed graphs.
        #for word in sentence:
        #    word['head'] = state['heads'][word['id']]
        #print(transitions)
        #print(state)
    print(X)
    #print(Y)