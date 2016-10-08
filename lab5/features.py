
import dparser
import transition



def extract(stack, queue, state, feature_names, sentence):
    """
     Extract the features from one sentence
     returns X and y, where X is a list of dictionaries and
     y is a list of symbols
     :param sentence:
     :param w_size:
     :return:
     """
    x = []
    tmpListStack = ['nil','nil','nil','nil']
    tmpListQueue = ['nil', 'nil','nil','nil']
    try:
        tmpListStack[0] = stack[0]['form']
        tmpListStack[1] = stack[0]['postag']
        tmpListStack[2] = stack[1]['form']
        tmpListStack[3] = stack[1]['postag']
    except:
        pass
    try:
        tmpListQueue[0] = queue[0]['form']
        tmpListQueue[1] = queue[0]['postag']
        tmpListQueue[2] = queue[1]['form']
        tmpListQueue[3] = queue[1]['postag']
    except:
        pass
    x.extend(tmpListStack)
    x.extend(tmpListQueue)
    x.append(transition.can_rightarc(stack))
    x.append(transition.can_reduce(stack,state))
    # We represent the feature vector as a dictionary
    # The classes are stored in a list
    #y.append(padded_sentence[i + w_size][2])
    return dict(zip(feature_names, x))

def extract2(stack, queue, state, feature_names, sentence):
    """
     Extract the features from one sentence
     returns X and y, where X is a list of dictionaries and
     y is a list of symbols
     :param sentence:
     :param w_size:
     :return:
     """
    tmpsiblings = ['nil', 'nil']
    left = 0
    right = 1000
    if(len(stack)>0 and len(state)>0):
        #print(state['heads'])
        for key,value in (state['heads'].items()):
            if(int(key)<int(stack[0]['id']) and int(value) == int(stack[0]['head'])):
                #print(str(key)+' ' + str(value))
                #print(stack[0]['id'])
                if left < int(key):
                    left = int(key)
            elif int(key) > int(stack[0]['id']) and int(value) == int(stack[0]['head']):
                if right > int(key):
                    right = int(key)
        if right< 1000:
            #print('right')
            #print(stack[0]['form'])
            #print(sentence[right]['form'])
            tmpsiblings[1] = sentence[right]['form']
            pass
        if(left >0):
            #print('left')
            #print(stack[0]['form'])
            #print(sentence[left]['form'])
            tmpsiblings[0] = sentence[left]['form']
            pass
            #if(indx < stack[0]['id'] and head):
        #print(sentence[stack[0]['id']+1])
        #while(head > 0):
        #   print(stack[0]['head'])
    x = []
    tmpListStack = ['nil','nil','nil','nil']
    tmpListQueue = ['nil', 'nil','nil','nil']
    tmpNextWord = ['nil','nil']


    try:
        tmpNextWord[1] = sentence[int(stack[0]['id']) + 1]['postag']
        tmpNextWord[1] = sentence[int(stack[0]['id']) + 1]['form']
    except:
        pass
    try:
        tmpListStack[0] = stack[0]['form']
        tmpListStack[1] = stack[0]['postag']
        tmpListStack[2] = stack[1]['form']
        tmpListStack[3] = stack[1]['postag']
    except:
        pass
    try:
        tmpListQueue[0] = queue[0]['form']
        tmpListQueue[1] = queue[0]['postag']
        tmpListQueue[2] = queue[1]['form']
        tmpListQueue[3] = queue[1]['postag']
    except:
        pass
    x.extend(tmpListStack)
    x.extend(tmpListQueue)
    x.append(transition.can_rightarc(stack))
    x.append(transition.can_reduce(stack,state))
    x.extend(tmpNextWord)
    x.extend(tmpsiblings)
    # We represent the feature vector as a dictionary
    # The classes are stored in a list
    #y.append(padded_sentence[i + w_size][2])
    return dict(zip(feature_names, x))