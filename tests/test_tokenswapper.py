from collections import namedtuple
from megaphone_tokenizer import tokenswapper as ts

class TestTokenSwapper():
        
    def test_swap_all_nested_itemnames_to_placeholder__WhenBracketSequenceWasReversed_ItemNamesShouldBeEmpty_TextShouldBeNoChange(self):
        inputText = '버서커 폭주플티 ]극찬클레압셋[ 팜ㅍㅍㅍㅍㅍㅍㅍ / 암제 블랙미러플티 극찬클레압셋 ㅍㅍㅍㅍㅍ'
        itemNames, processedText = ts._swap_all_nested_itemnames_to_placeholder(inputText)
        assert itemNames == []
        assert processedText == inputText

    def test_swap_all_nested_itemnames_to_placeholder__WhenContainsSingleItemName_ShouldBeReturned(self):
        T = namedtuple('T', 'itemName, formatString')
        testList = [
            T('[시로코]', '{itemName}팔라딘4차 극찬뚫피포함 1.4에팜/수인족 칭호상자 5개 개당1450 세라상자 개당110 5개삼 ㅅㅅ'), 
            T('[ 11 화둔 : 염화멸섬]','{itemName} 2400팝니다~~~~~~~~~~~~~~~~~~~~~~~~~'),
            T('[블랙네뷸라 원석 상의]','체홀 11차레압 극찬 뚫피포힘 4500에팝니다{itemName}ㅍㅍㅍㅍㅍ'),
            T('[30프로 10 장비 증폭권 ( 30일 )]','{itemName} 1650팜')
        ]

        for test in testList:
            itemNames, processedText = ts._swap_all_nested_itemnames_to_placeholder(test.formatString.format(itemName=test.itemName))
            assert len(itemNames) == 1
            assert itemNames == [test.itemName]
            assert processedText == test.formatString.format(itemName=' ' + ts.PLACEHOLDER + '0 ')

    def test_swap_all_nested_itemnames_to_placeholder__WhenContainsMultipleItemnames_ShouldBeReturned(self):
        T = namedtuple('T', 'itemNames, formatString')
        testList = [
            T(['[레어 상의 클론 아바타]', '[레어 하의 클론 아바타]'],'{0}{1} 신검플티 상하의 팝니다 7800 드립니다 애누리없')
        ]

        for test in testList:
            inputText = test.formatString
            for i in range(0, len(test.itemNames)):
                inputText = inputText.replace('{' + str(i) + '}', test.itemNames[i])
            itemNames, processedText = ts._swap_all_nested_itemnames_to_placeholder(inputText)
            assert len(itemNames) == len(test.itemNames)
            assert itemNames == test.itemNames
            expectedProcessedText = test.formatString
            for i in range(0, len(test.itemNames)):
                expectedProcessedText = expectedProcessedText.replace('{' + str(i) + '}', ' ' + ts.PLACEHOLDER + str(i) + ' ')
            assert processedText == expectedProcessedText
    
    def test_swap_all_nested_itemnames_to_placeholder__WhenThreeDepthItemNames_ShouldBeReturned(self):
        T = namedtuple('T', 'input, itemNames, processedText')
        testList = [
            T(
                '[[4월]10프로 12 장비 증폭권][[4월]30프로 10 장비 증폭권] 2개 4800에 팜 트레 주셈',
                ['[4월]', '[4월]', '[ InnerItemNamePlaceHolder0 10프로 12 장비 증폭권]', '[ InnerItemNamePlaceHolder0 30프로 10 장비 증폭권]'],
                ' ItemNamePlaceHolder2  ItemNamePlaceHolder3  2개 4800에 팜 트레 주셈'
            ),
            T(
                '[[4월[2일]]10프로 12 장비 증폭권][[4월[3일]]30프로 10 장비 증폭권] 2개 4800에 팜 트레 주셈',
                ['[2일]', '[3일]', '[4월 InnerItemNamePlaceHolder0 ]', '[4월 InnerItemNamePlaceHolder1 ]', '[ InnerItemNamePlaceHolder2 10프로 12 장비 증폭권]', '[ InnerItemNamePlaceHolder3 30프로 10 장비 증폭권]'],
                ' ItemNamePlaceHolder4  ItemNamePlaceHolder5  2개 4800에 팜 트레 주셈'
            )
        ]

        for test in testList:
            itemNames, processedText = ts._swap_all_nested_itemnames_to_placeholder(test.input)
            assert itemNames == test.itemNames
            assert processedText == test.processedText
    
    def test_recover_nested_itemname_WhenThereWasNoNestedItemNames_ShouldBeNochange(self):
        assert ['test'] == ts._recover_nested_itemname(['test'])
        assert ['[itemName1]', '[itemName2]'] == ts._recover_nested_itemname(['[itemName1]','[itemName2]'])
    
    def test_recover_nested_itemname_WhenContainsNestedItemName_ShouldBeRecovered(self):
        assert ['[nested]', '[[nested]parent]'] == ts._recover_nested_itemname(['[nested]', '[ ' + ts.INNER_PLACEHOLDER + '0 parent]'])
    
    def test_recover_nested_itemname_WhenContainsMultiDepthNestedItemName_ShouldBeRecovered(self):
        expected = ['[nested2]', '[nested1[nested2]parent2]', '[[nested1[nested2]parent2]parent1]']
        actual = ts._recover_nested_itemname(['[nested2]', '[nested1 ' + ts.INNER_PLACEHOLDER + '0 parent2]', '[ ' + ts.INNER_PLACEHOLDER + '1 parent1]'])
        assert actual == expected
    
    def test_recover_placeholders(self):
        tokens = [(ts.PLACEHOLDER, 'Noun'), ('0', 'Number'), ('팔라딘', 'Noun')]
        placeHolderDic = ['[시로코]']
        actual = ts.recover_placeholders(tokens, placeHolderDic)
        assert actual == [('[시로코]', ts.POS_TAG_ITEM_NAME), ('팔라딘', 'Noun')]
    
    def test_swap_to_placeholder_WhenTextDoesNotContainsItemName_PlaceHolderDicShouldBeNone_TextShouldBeNoChange(self):
        placeHolderDic, swappedText = ts.swap_to_placeholder('2개 4800에 팜 트레 주셈')
        assert placeHolderDic is None
        assert swappedText == '2개 4800에 팜 트레 주셈'

    def test_swap_to_placeholder(self):
        placeHolderDic, swappedText = ts.swap_to_placeholder('[[4월 [2일]]10프로 12 장비 증폭권][[4월 [3일]]30프로 10 장비 증폭권] 2개 4800에 팜 트레 주셈')
        assert placeHolderDic == ['[2일]', '[3일]', '[4월 [2일]]', '[4월 [3일]]', '[[4월 [2일]]10프로 12 장비 증폭권]', '[[4월 [3일]]30프로 10 장비 증폭권]']
        assert swappedText == ' ItemNamePlaceHolder4  ItemNamePlaceHolder5  2개 4800에 팜 트레 주셈'
