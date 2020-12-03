import re

text = '''your name in lower letters@ the name of the internet provider example

Well, janedoeentrprise@bell.com this is just example you do not have to use your own name you can use the name of your company if you have one. OR any name that comes to mind as long as you have the correct internet providers address

Even if “baseballbro25@aim.com” serves as a nostalgic reminder for your peak athletic years, it’ll look like an eyesore on your resume and prompt any recruiter or hiring manager to press delete.

A specific example is jsmith@example.com. Thus, an address consists of two principal parts, a username and a domain name. The domain name is used to transport a mail message to the host of the recipient's mail system.

simple@example.com
very.common@example.com
disposable.style.email.with+symbol@example.com
other.email-with-hyphen@example.com
fully-qualified-domain@example.com
x@example.com (one-letter local-part)
example-indeed@strange-example.com
" "@example.org (space between the quotes)
"john..doe"@example.org (quoted double dot)
mailhost!username@example.org (bangified host route used for uucp mailers)
Gmail ignores all dots in the local-part of a @gmail.com address for the purposes of determining account identity.[12] The example addresses below would not be handled by RFC 5322 based servers, but are permitted by RFC 6530. Servers compliant with this will be able to handle these:

Latin alphabet with diacritics: Pelé@example.com
Greek alphabet: δοκιμή@παράδειγμα.δοκιμή
Traditional Chinese characters: 我買@屋企.香港
Japanese characters: 二ノ宮@黒川.日本
Cyrillic characters: медведь@с-балалайкой.рф
Devanagari characters: संपर्क@डाटामेल.भारत'''

# variables just for reference
latin_chars = 'a-zA-Z'
rus_chars = 'а-яА-Я'
greek_chars = 'α-ωΑ-ΩίϊΐόάέύϋΰήώΊΪΌΆΈΎΫΉΏ'
accented_chars = 'À-ÖØ-öø-ÿ'
special_signs = '\"\-\.\+!'
nums = '0-9'
china_japan_kanji_chars = u'\u4E00-\u9FFF'
japan_hiragana_chars = u'\u3040-\u309F'
japan_katakana = '\u30A0-\u30FF'
devangari_chars = '\u0900-\u097F'

emails = re.findall(r'[a-zA-Zа-яА-Яα-ωΑ-ΩίϊΐόάέύϋΰήώΊΪΌΆΈΎΫΉΏÀ-ÖØ-öø-ÿ\"\-\.\+!0-9\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF\u0900-\u097F]{1,}@[a-zA-Zа-яА-Яα-ωΑ-ΩίϊΐόάέύϋΰήώΊΪΌΆΈΎΫΉΏÀ-ÖØ-öø-ÿ\"\-\.\+!0-9\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF\u0900-\u097F]*\.[a-zA-Zа-яА-Яα-ωΑ-ΩίϊΐόάέύϋΰήώΊΪΌΆΈΎΫΉΏÀ-ÖØ-öø-ÿ\"\-\.\+!0-9\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF\u0900-\u097F]{1,}', text, re.UNICODE)
# print(emails)

# idea for explicit solution - f_strings or string formatting - doesn't allow conditions {1,} - from 1 to n. Suppose need double {{ }} escaping. TODO - check this issue:
# result = re.findall(r'[{latin}{rus}{greek}{accented}{japan}{devangari}{signs}{nums}]*@[{latin}{rus}{accented}{greek}{japan}{devangari}{signs}{nums}]*\.[{latin}{rus}{greek}{accented}{japan}{devangari}{signs}{nums}]*'.format(latin=latin_chars, rus=rus_chars, greek=greek_chars, accented=accented_chars, japan=china_japan_kanji_chars, signs=special_signs, nums=nums, devangari=devangari_chars), text, re.UNICODE)
# print(result)

###################################
######### filtering out wrong emails like: ' '@gmail.com, "@gmail.com, etc.
###################################

r = re.compile(r'\"@[a-zA-Zа-яА-Яα-ωΑ-ΩίϊΐόάέύϋΰήώΊΪΌΆΈΎΫΉΏÀ-ÖØ-öø-ÿ\"\-\.\+!0-9\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF\u0900-\u097F]*\.[a-zA-Zа-яА-Яα-ωΑ-ΩίϊΐόάέύϋΰήώΊΪΌΆΈΎΫΉΏÀ-ÖØ-öø-ÿ\"\-\.\+!0-9\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF\u0900-\u097F]{1,}')
wrong_emails = list(filter(r.match, emails)) # Read Note

filtered_emails = [x for x in emails if x not in wrong_emails]
unique_emails = set(filtered_emails)


###################################
######### Processign domains
###################################

domains = re.findall(r'@[a-zA-Zа-яА-Яα-ωΑ-ΩίϊΐόάέύϋΰήώΊΪΌΆΈΎΫΉΏÀ-ÖØ-öø-ÿ\"\-\.\+!0-9\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF\u0900-\u097F]*\.[a-zA-Zа-яА-Яα-ωΑ-ΩίϊΐόάέύϋΰήώΊΪΌΆΈΎΫΉΏÀ-ÖØ-öø-ÿ\"\-\.\+!0-9\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF\u0900-\u097F]{1,}', text, re.UNICODE)

# delete trailing comma as in 'example.com.'
domains = [x.lstrip('@').rstrip('.') for x in domains]
unique_domains = set(domains)

print()
print('==='*10)
print('Unique emails count', len(unique_emails))
print(unique_emails)

print()
print('==='*10)
print('Unique domains count:', len(unique_domains))
print(unique_domains)