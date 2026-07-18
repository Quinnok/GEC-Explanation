# ERRANT vs Token Diff Check

This report is generated automatically from real EXPECT source/reference pairs.

## 1. expect-test-00000

- Source: `In my community , we are very interested at the environment and ecological things .`
- Reference: `In my community , we are very interested in the environment and ecological things .`
- EXPECT type: `Preposition`
- ERRANT edits: `[{"start": 8, "end": 9, "source_text": "at", "target_text": "in", "operation": "replace", "error_type": "R:PREP"}]`
- Token-diff edits: `[{"start": 8, "end": 9, "source_text": "at", "target_text": "in", "operation": "replace", "error_type": "Preposition"}]`

## 2. expect-test-00001

- Source: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer ed finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- Reference: `Technology has chanched people 's lives a lot . In fact we can think how different is our life compared either to our parents ' or our grandparents ' lives . For example my parents did n't watch tv , because there was n't any tv in the world when they were young.but that is n't the only difference : we can think about the mobile phone , the computer and finally the internet.our grandparents could n't have imagined a strange machine like the computer in their lives .`
- EXPECT type: `Others`
- ERRANT edits: `[{"start": 70, "end": 71, "source_text": "ed", "target_text": "and", "operation": "replace", "error_type": "R:OTHER"}]`
- Token-diff edits: `[{"start": 70, "end": 71, "source_text": "ed", "target_text": "and", "operation": "replace", "error_type": "Others"}]`

## 3. expect-test-00002

- Source: `We should use of public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- Reference: `We should use public transport because at the present there are a lot of cars in the world that pollute and unfortunately we are harming the environment and the world .`
- EXPECT type: `Preposition`
- ERRANT edits: `[{"start": 3, "end": 4, "source_text": "of", "target_text": "", "operation": "delete", "error_type": "U:PREP"}]`
- Token-diff edits: `[{"start": 3, "end": 4, "source_text": "of", "target_text": "", "operation": "delete", "error_type": "Preposition"}]`

## 4. expect-test-00003

- Source: `Although there are many positive points about private cars , they are also negative ones .`
- Reference: `Although there are many positive points about private cars , there are also negative ones .`
- EXPECT type: `Others`
- ERRANT edits: `[{"start": 10, "end": 11, "source_text": "they", "target_text": "there", "operation": "replace", "error_type": "R:PRON"}]`
- Token-diff edits: `[{"start": 10, "end": 11, "source_text": "they", "target_text": "there", "operation": "replace", "error_type": "Others"}]`

## 5. expect-test-00004

- Source: `However , public transportation is much cheaper than buying a new car and for the adventurer who wants to have an exciting travel for then to see more action .`
- Reference: `However , public transportation is much cheaper than buying a new car and for the adventurer who wants to have an exciting journey for then to see more action .`
- EXPECT type: `Collocation`
- ERRANT edits: `[{"start": 22, "end": 23, "source_text": "travel", "target_text": "journey", "operation": "replace", "error_type": "R:NOUN"}]`
- Token-diff edits: `[{"start": 22, "end": 23, "source_text": "travel", "target_text": "journey", "operation": "replace", "error_type": "Collocation"}]`

## 6. expect-test-00005

- Source: `They were planning to steal a very precious thing from Museum tonight .`
- Reference: `They were planning to steal a very precious thing from a Museum tonight .`
- EXPECT type: `Article`
- ERRANT edits: `[{"start": 10, "end": 10, "source_text": "", "target_text": "a", "operation": "insert", "error_type": "M:DET"}]`
- Token-diff edits: `[{"start": 10, "end": 10, "source_text": "", "target_text": "a", "operation": "insert", "error_type": "Article"}]`

## 7. expect-test-00006

- Source: `I hope my house will win the champion next year .`
- Reference: `I hope my house will win the championship next year .`
- EXPECT type: `Collocation`
- ERRANT edits: `[{"start": 7, "end": 8, "source_text": "champion", "target_text": "championship", "operation": "replace", "error_type": "R:MORPH"}]`
- Token-diff edits: `[{"start": 7, "end": 8, "source_text": "champion", "target_text": "championship", "operation": "replace", "error_type": "Collocation"}]`

## 8. expect-test-00007

- Source: `In conclusion , I think that this type of food and atmosphere is very for us , because normally we speak about books , work and studies , whereas with this type of environment we can speak about ourselves , our family , our hobbies and everyone will get to know new something about other classmates .`
- Reference: `In conclusion , I think that this type of food and atmosphere is very good for us , because normally we speak about books , work and studies , whereas with this type of environment we can speak about ourselves , our family , our hobbies and everyone will get to know new something about other classmates .`
- EXPECT type: `Others`
- ERRANT edits: `[{"start": 14, "end": 14, "source_text": "", "target_text": "good", "operation": "insert", "error_type": "M:ADJ"}]`
- Token-diff edits: `[{"start": 14, "end": 14, "source_text": "", "target_text": "good", "operation": "insert", "error_type": "Others"}]`

## 9. expect-test-00008

- Source: `I 'd like to tell you about my favorite restaurant its name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an Excellent choice for me and My favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .`
- Reference: `I 'd like to tell you about my favorite restaurant . It 's name is " Lemon " I go there every week it has different food to other restaurants I 'd like chicken crispy with garlic sauce It 's an Excellent choice for me and My favorite appitizer is susage and in order that dessert I 'd like " Vadge " cake with chocolate sauce I feel at ease when I go there I enjoy classical music while having lunch about the service It 's very good and all the staff are respectable I ca n't imagine one week without going there that would drive me nuts I advise everyone to go there and enjoy their time there , also this restaurant has a relative advantage in hygiene really It 's excellent The striking thing for anyone despite all of these advantages the prices are not expensive .`
- EXPECT type: `Others`
- ERRANT edits: `[{"start": 10, "end": 10, "source_text": "", "target_text": ".", "operation": "insert", "error_type": "M:PUNCT"}, {"start": 10, "end": 11, "source_text": "its", "target_text": "It 's", "operation": "replace", "error_type": "R:OTHER"}]`
- Token-diff edits: `[{"start": 10, "end": 11, "source_text": "its", "target_text": ". It 's", "operation": "replace", "error_type": "Others"}]`

## 10. expect-test-00009

- Source: `But such a high level of development of Egyptian civilization has a negative side as well as positive .`
- Reference: `But such a high level of development of Egyptian civilization has a negative side as well as a positive .`
- EXPECT type: `Article`
- ERRANT edits: `[{"start": 17, "end": 17, "source_text": "", "target_text": "a", "operation": "insert", "error_type": "M:DET"}]`
- Token-diff edits: `[{"start": 17, "end": 17, "source_text": "", "target_text": "a", "operation": "insert", "error_type": "Article"}]`

## 11. expect-test-00010

- Source: `Until dawn all of them had got out , so they sacred until they found a refuge .`
- Reference: `By dawn all of them had got out , so they sacred until they found a refuge .`
- EXPECT type: `Collocation`
- ERRANT edits: `[{"start": 0, "end": 1, "source_text": "Until", "target_text": "By", "operation": "replace", "error_type": "R:PREP"}]`
- Token-diff edits: `[{"start": 0, "end": 1, "source_text": "Until", "target_text": "By", "operation": "replace", "error_type": "Collocation"}]`

## 12. expect-test-00011

- Source: `What a wonderful day ! There is April now and finally spring has come .`
- Reference: `What a wonderful day ! It is April now and finally spring has come .`
- EXPECT type: `Others`
- ERRANT edits: `[{"start": 5, "end": 6, "source_text": "There", "target_text": "It", "operation": "replace", "error_type": "R:PRON"}]`
- Token-diff edits: `[{"start": 5, "end": 6, "source_text": "There", "target_text": "It", "operation": "replace", "error_type": "Others"}]`

## 13. expect-test-00012

- Source: `The traffic can affect cars and buses at the same extent .`
- Reference: `The traffic can affect cars and buses to the same extent .`
- EXPECT type: `Preposition`
- ERRANT edits: `[{"start": 7, "end": 8, "source_text": "at", "target_text": "to", "operation": "replace", "error_type": "R:PREP"}]`
- Token-diff edits: `[{"start": 7, "end": 8, "source_text": "at", "target_text": "to", "operation": "replace", "error_type": "Preposition"}]`

## 14. expect-test-00013

- Source: `Computers have had a most significant impact on the people in the latter 1/2 of the 20th century .`
- Reference: `Computers have had a most significant impact on people in the latter 1/2 of the 20th century .`
- EXPECT type: `Article`
- ERRANT edits: `[{"start": 8, "end": 9, "source_text": "the", "target_text": "", "operation": "delete", "error_type": "U:DET"}]`
- Token-diff edits: `[{"start": 8, "end": 9, "source_text": "the", "target_text": "", "operation": "delete", "error_type": "Article"}]`

## 15. expect-test-00014

- Source: `i love my family especially my little sister , she has sixteen years old , i consider her my best friend because i usually tell her everything about my life .`
- Reference: `i love my family especially my little sister , she is sixteen years old , i consider her my best friend because i usually tell her everything about my life .`
- EXPECT type: `Collocation`
- ERRANT edits: `[{"start": 10, "end": 11, "source_text": "has", "target_text": "is", "operation": "replace", "error_type": "R:VERB"}]`
- Token-diff edits: `[{"start": 10, "end": 11, "source_text": "has", "target_text": "is", "operation": "replace", "error_type": "Collocation"}]`

## 16. expect-test-00015

- Source: `Technology will have advanced and maybe the cars will fly above streets and computers will have totally changed .`
- Reference: `Technology will have advanced and maybe cars will fly above streets and computers will have totally changed .`
- EXPECT type: `Article`
- ERRANT edits: `[{"start": 6, "end": 7, "source_text": "the", "target_text": "", "operation": "delete", "error_type": "U:DET"}]`
- Token-diff edits: `[{"start": 6, "end": 7, "source_text": "the", "target_text": "", "operation": "delete", "error_type": "Article"}]`

## 17. expect-test-00016

- Source: `In the end I think if many people want the Monarchy to be ablished a general election should be called and then see if the Monarchy should be abolished .`
- Reference: `In the end I think if many people want the Monarchy to be abolished , a general election should be called and then see if the Monarchy should be abolished .`
- EXPECT type: `Others`
- ERRANT edits: `[{"start": 13, "end": 14, "source_text": "ablished", "target_text": "abolished", "operation": "replace", "error_type": "R:SPELL"}, {"start": 14, "end": 14, "source_text": "", "target_text": ",", "operation": "insert", "error_type": "M:PUNCT"}]`
- Token-diff edits: `[{"start": 13, "end": 14, "source_text": "ablished", "target_text": "abolished ,", "operation": "replace", "error_type": "Others"}]`

## 18. expect-test-00017

- Source: `Sometimes we go to partyies in the city , I dance in the parties with my friends .`
- Reference: `Sometimes we go to partyies in the city , I dance at the parties with my friends .`
- EXPECT type: `Preposition`
- ERRANT edits: `[{"start": 11, "end": 12, "source_text": "in", "target_text": "at", "operation": "replace", "error_type": "R:PREP"}]`
- Token-diff edits: `[{"start": 11, "end": 12, "source_text": "in", "target_text": "at", "operation": "replace", "error_type": "Preposition"}]`

## 19. expect-test-00018

- Source: `I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring of the environment is very important and in my village they take different actions to care for it .`
- Reference: `I live in San Miguel Almoloyan , this is a village in the municipality of Almoloya de Juarez in the State of Mexico . Caring for the environment is very important and in my village they take different actions to care for it .`
- EXPECT type: `Preposition`
- ERRANT edits: `[{"start": 25, "end": 26, "source_text": "of", "target_text": "for", "operation": "replace", "error_type": "R:PREP"}]`
- Token-diff edits: `[{"start": 25, "end": 26, "source_text": "of", "target_text": "for", "operation": "replace", "error_type": "Preposition"}]`

## 20. expect-test-00019

- Source: `we think that in the future the planet will be in a bad condition and the trees will be dissappearing , after that we will have wars .`
- Reference: `we think that in the future the planet will be in a bad condition and the trees will disappear , after that we will have wars .`
- EXPECT type: `POS Confusion`
- ERRANT edits: `[{"start": 18, "end": 20, "source_text": "be dissappearing", "target_text": "disappear", "operation": "replace", "error_type": "R:VERB"}]`
- Token-diff edits: `[{"start": 18, "end": 20, "source_text": "be dissappearing", "target_text": "disappear", "operation": "replace", "error_type": "POS Confusion"}]`

## 21. expect-test-00020

- Source: `First , the scene that described the murder makes readers unable to stop themselves imagining the images in their mind .`
- Reference: `First , the scene that described the murder makes readers unable to stop themselves imagining the images in their minds .`
- EXPECT type: `Number`
- ERRANT edits: `[{"start": 19, "end": 20, "source_text": "mind", "target_text": "minds", "operation": "replace", "error_type": "R:NOUN:NUM"}]`
- Token-diff edits: `[{"start": 19, "end": 20, "source_text": "mind", "target_text": "minds", "operation": "replace", "error_type": "Number"}]`

## 22. expect-test-00021

- Source: `Additionally , people now continue to destroy more agricultures and forest in order to satisfy all their needs , which will distory the ecosystem diversity and biodiversity especially the endangered species .`
- Reference: `Additionally , people now continue to destroy more agricultural land and forest in order to satisfy all their needs , which will distory the ecosystem diversity and biodiversity especially the endangered species .`
- EXPECT type: `Others`
- ERRANT edits: `[{"start": 8, "end": 9, "source_text": "agricultures", "target_text": "agricultural", "operation": "replace", "error_type": "R:SPELL"}, {"start": 9, "end": 9, "source_text": "", "target_text": "land", "operation": "insert", "error_type": "M:NOUN"}]`
- Token-diff edits: `[{"start": 8, "end": 9, "source_text": "agricultures", "target_text": "agricultural land", "operation": "replace", "error_type": "Others"}]`

## 23. expect-test-00022

- Source: `The city has many projects such as " Keep it clean , keep it beauty " , the goal of which is to promote proper disposal in the public areas .`
- Reference: `The city has many projects such as " Keep it clean , keep it beautiful " , the goal of which is to promote proper disposal in the public areas .`
- EXPECT type: `POS Confusion`
- ERRANT edits: `[{"start": 14, "end": 15, "source_text": "beauty", "target_text": "beautiful", "operation": "replace", "error_type": "R:MORPH"}]`
- Token-diff edits: `[{"start": 14, "end": 15, "source_text": "beauty", "target_text": "beautiful", "operation": "replace", "error_type": "POS Confusion"}]`

## 24. expect-test-00023

- Source: `The AVE or aeroplane are a good option for long trips .`
- Reference: `The AVE or aeroplane is a good option for long trips .`
- EXPECT type: `Subject-Verb Agreement`
- ERRANT edits: `[{"start": 4, "end": 5, "source_text": "are", "target_text": "is", "operation": "replace", "error_type": "R:VERB:SVA"}]`
- Token-diff edits: `[{"start": 4, "end": 5, "source_text": "are", "target_text": "is", "operation": "replace", "error_type": "Subject-Verb Agreement"}]`

## 25. expect-test-00024

- Source: `I really enjoy it because the plot is original and it shows different life stories of moving characters .`
- Reference: `I really enjoy it because the plot is original and it shows the different life stories of moving characters .`
- EXPECT type: `Article`
- ERRANT edits: `[{"start": 12, "end": 12, "source_text": "", "target_text": "the", "operation": "insert", "error_type": "M:DET"}]`
- Token-diff edits: `[{"start": 12, "end": 12, "source_text": "", "target_text": "the", "operation": "insert", "error_type": "Article"}]`

## 26. expect-test-00025

- Source: `All the household nearby the public road throw dirty things away easily and even do n't bother about the order of the municipality .`
- Reference: `All the households nearby the public road throw dirty things away easily and even do n't bother about the order of the municipality .`
- EXPECT type: `Number`
- ERRANT edits: `[{"start": 2, "end": 3, "source_text": "household", "target_text": "households", "operation": "replace", "error_type": "R:NOUN:NUM"}]`
- Token-diff edits: `[{"start": 2, "end": 3, "source_text": "household", "target_text": "households", "operation": "replace", "error_type": "Number"}]`

## 27. expect-test-00026

- Source: `Since the units were sold in inventory but your purchase indicates that 6 pieces were confirmed , do not worry about it , we will send you the remaining unit as soon as possible .`
- Reference: `Since the units were sold in the inventory but your purchase indicates that 6 pieces were confirmed , do not worry about it , we will send you the remaining unit as soon as possible .`
- EXPECT type: `Article`
- ERRANT edits: `[{"start": 6, "end": 6, "source_text": "", "target_text": "the", "operation": "insert", "error_type": "M:DET"}]`
- Token-diff edits: `[{"start": 6, "end": 6, "source_text": "", "target_text": "the", "operation": "insert", "error_type": "Article"}]`

## 28. expect-test-00027

- Source: `Everyone should develop their awareness of public manner .`
- Reference: `Everyone should develop their awareness of public manners .`
- EXPECT type: `Number`
- ERRANT edits: `[{"start": 7, "end": 8, "source_text": "manner", "target_text": "manners", "operation": "replace", "error_type": "R:NOUN:NUM"}]`
- Token-diff edits: `[{"start": 7, "end": 8, "source_text": "manner", "target_text": "manners", "operation": "replace", "error_type": "Number"}]`

## 29. expect-test-00028

- Source: `A worldwide war is the only case in which we would see a dramatic change in peoples lives in the time length of 50 years from now .`
- Reference: `A worldwide war is the only case in which we would see a dramatic change in peoples lives in the period of 50 years from now .`
- EXPECT type: `Collocation`
- ERRANT edits: `[{"start": 20, "end": 22, "source_text": "time length", "target_text": "period", "operation": "replace", "error_type": "R:NOUN"}]`
- Token-diff edits: `[{"start": 20, "end": 22, "source_text": "time length", "target_text": "period", "operation": "replace", "error_type": "Collocation"}]`

## 30. expect-test-00029

- Source: `According to l'Academie Français , all literature of the Neoclassic period must follow the rules of propriety which regulated the author should avoid certain topics , including sex , violence , church , and state issues .`
- Reference: `According to l'Academie Français , all literature of the Neoclassical period must follow the rules of propriety which regulated the author should avoid certain topics , including sex , violence , church , and state issues .`
- EXPECT type: `Collocation`
- ERRANT edits: `[{"start": 9, "end": 10, "source_text": "Neoclassic", "target_text": "Neoclassical", "operation": "replace", "error_type": "R:MORPH"}]`
- Token-diff edits: `[{"start": 9, "end": 10, "source_text": "Neoclassic", "target_text": "Neoclassical", "operation": "replace", "error_type": "Collocation"}]`

