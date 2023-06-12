import os

from os import path
from wordcloud import WordCloud

text="""Narendra Damodardas Modi (Gujarati: [ˈnəɾendɾə dɑmodəɾˈdɑs ˈmodiː] (listen); born 17 September 1950)[b] is an Indian politician who has served as the 14th Prime Minister of India since May 2014. Modi was Chief Minister of Gujarat from 2001 to 2014 and is the Member of Parliament (MP) for Varanasi. He is a member of the Bharatiya Janata Party (BJP) and of the Rashtriya Swayamsevak Sangh (RSS), a right-wing Hindu nationalist paramilitary volunteer organisation. He is the longest-serving prime minister from outside the Indian National Congress.

Modi was born and raised in Vadnagar in northeastern Gujarat, where he completed his secondary education. He was introduced to the RSS at age eight. His account of helping his father sell tea at the Vadnagar railway station has not been reliably corroborated. At age 18, he was married to Jashodaben Modi, whom he abandoned soon after, only publicly acknowledging her four decades later when legally required to do so. Modi became a full-time worker for the RSS in Gujarat in 1971. After the state of emergency was declared by Prime Minister Indira Gandhi in 1975, he went into hiding. The RSS assigned him to the BJP in 1985 and he held several positions within the party hierarchy until 2001, rising to the rank of general secretary.[c]

In 2001, Modi was appointed Chief Minister of Gujarat due to Keshubhai Patel's failing health and poor public image following the earthquake in Bhuj that year, and Modi was elected to the legislative assembly soon after. His administration is considered complicit in the 2002 Gujarat riots, in which over 1,000 people were killed—three-quarters of whom were Muslim—[d] and has been criticised for its management of the crisis. A Special Investigation Team appointed by the Supreme Court of India found no evidence to initiate prosecution proceedings against him.[e] While his policies as chief minister, which were credited for encouraging economic growth, were praised, Modi's administration was criticised for failing to significantly improve health, poverty and education indices in the state.[f]

Modi led the BJP in the 2014 Indian general election, in which the party gained a majority in the lower house of the Indian parliament the Lok Sabha; it was the first time for any single party since 1984. His administration has tried to raise direct foreign investment in the Indian economy, and reduced spending on healthcare, education, and social-welfare programmes. He centralised power by abolishing the Planning Commission and replacing it with the NITI Aayog. Modi began a high-profile sanitation campaign, controversially initiated the 2016 demonetisation of high-denomination banknotes and introduced the Goods and Services Tax, and weakened or abolished environmental and labour laws.

Modi's administration launched the 2019 Balakot airstrike against an alleged terrorist training camp in Pakistan: the airstrike failed,[12][13] but had nationalist appeal.[14] Modi's party comfortably won the 2019 general election which followed.[15] In its second term, his administration revoked the special status of Jammu and Kashmir, an Indian-administred portion of the disputed Kashmir region,[16][17] and introduced the Citizenship Amendment Act, prompting widespread protests, and spurring the 2020 Delhi riots in which Muslims were brutalized and killed by Hindu mobs,[18][19][20] sometimes with the complicity of police forces controlled by the Modi administration.[21][22] Three controversial farm laws, led to sit-ins by farmers across the country, eventually causing their formal repeal. Modi oversaw India's response to the COVID-19 pandemic, during which 4.7 million Indians died, according to the World Health Organization's estimates.[23][24]

Under Modi's tenure, India has experienced democratic backsliding, or the weakening of democratic institutions, individual rights, and freedom of expression.[25][26][g] As prime minister, he has received consistently high approval ratings.[32][33][34] Modi has been described as engineering a political realignment towards right-wing politics. He remains a controversial figure domestically and internationally, over his Hindu nationalist beliefs and handling of the 2002 Gujarat riots, which have been cited as evidence of a majoritarian and exclusionary social agenda.[h]"""

# Generate a word cloud image
wordcloud = WordCloud(background_color="white").generate(text)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
# wordcloud = WordCloud(max_font_size=40).generate(text)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
plt.savefig('./wc/test.jpeg')