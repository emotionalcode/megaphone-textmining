import re

REGX_BETWEEN_BRACKET = r'\[([^/[]*?)\]'
ITEMNAME_PARTICLE_PREFIX = "["
ITEMNAME_PARTICLE_SUFFIX = "]"
PLACEHOLDER = "ItemNamePlaceHolder"
INNER_PLACEHOLDER = "InnerItemNamePlaceHolder"
POS_TAG_ITEM_NAME = 'ItemName'

def swap_to_placeholder(text):
    """swap item name to placeholder.

    Returns: placeHolderDic, swappedText
    """

    # week check
    textDoesNotContainsItemName = not all(value in text for value in (ITEMNAME_PARTICLE_PREFIX, ITEMNAME_PARTICLE_SUFFIX))
    if textDoesNotContainsItemName:
        return None, text
    
    allNestedItemNames, swappedText = _swap_all_nested_itemnames_to_placeholder(text)
    placeHolderDic = _recover_nested_itemname(allNestedItemNames)
    return placeHolderDic, swappedText
    
def recover_placeholders(tokens, placeHolderDic):
    """re-swap placeholders to item name.

    Returns: recovered tokens
    """
    recoveredTokens = []
    for i, token in enumerate(tokens):
        if i > 0 and tokens[i-1][0] == PLACEHOLDER:
            continue
        if token[0] == PLACEHOLDER and i+1 < len(tokens):
            sequenceOfPlaceHolder = int(tokens[i + 1][0]) #next token is placeholder's seq number
            recoveredTokens.append((placeHolderDic[sequenceOfPlaceHolder], POS_TAG_ITEM_NAME))
        else:
            recoveredTokens.append(tokens[i])
    return recoveredTokens

def _swap_all_nested_itemnames_to_placeholder(text):
    allNestedItemNames = []
    pattern = re.compile(REGX_BETWEEN_BRACKET)
    numberOfMatch = len(pattern.findall(text))
    while numberOfMatch > 0:
        for match in pattern.finditer(text):
            itemName = match.group()
            text = text.replace(itemName, ' ' + PLACEHOLDER + str(len(allNestedItemNames)) + ' ')
            itHasNestedItemName = PLACEHOLDER in itemName
            if itHasNestedItemName:
                itemName = itemName.replace(PLACEHOLDER, INNER_PLACEHOLDER)
            allNestedItemNames.append(itemName)
        numberOfMatch = len(pattern.findall(text))
    return allNestedItemNames, text

def _recover_nested_itemname(allNestedItemNames):
    for i, particle in enumerate(allNestedItemNames):
        itHasNestedItemName = INNER_PLACEHOLDER in particle
        if itHasNestedItemName:
            idxNestedItemName = re.search(r'\d+', re.search(PLACEHOLDER + r'\d+', particle).group()).group()
            allNestedItemNames[i] = particle.replace(' ' + INNER_PLACEHOLDER + idxNestedItemName + ' ', allNestedItemNames[int(idxNestedItemName)])
    return allNestedItemNames

# def _get_outermost_item_names(txt, particles):
#     itemNames = []
#     for placeHolderMatch2 in re.finditer("(" + PLACEHOLDER + r"\d+)", txt):
#         placeHolder = placeHolderMatch2.group()
#         index = re.search(r'\d+', placeHolder).group()
#         txt = txt.replace(placeHolder, PLACEHOLDER + str(len(itemNames)))
#         itemNames.append(particles[int(index)])
#     return itemNames, txt