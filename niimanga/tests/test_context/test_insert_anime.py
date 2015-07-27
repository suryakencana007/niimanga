"""
 # Copyright (c) 05 2015 | surya
 # 06/05/15 nanang.ask@kubuskotak.com
 # This program is free software; you can redistribute it and/or
 # modify it under the terms of the GNU General Public License
 # as published by the Free Software Foundation; either version 2
 # of the License, or (at your option) any later version.
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # GNU General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License
 # along with this program; if not, write to the Free Software
 # Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 #  test_insert_anime.py
"""
from niimanga.models.master import Season


def test_anime():
    season_qry = Season.query
    spring = season_qry.filter(Season.slug == "anime-spring-2015").first()


    punchline = Video("Punch Line", "Comedy, Ecchi, Slice of Life",
                      synopsis="If he sees underwear, humanity will be destroyed!? An original anime series from the noitaminA block, Punchline centers on Yuuta Iridatsu, a high school student, with a peculiar habit. When he sees a girl's panties, he gets so excited he faints! After a certain incident with a ghost cat, his soul gets separated from his body. Using his special powers, Yuuta watches the daily lives of the inhabitants of an apartment and sometimes plays tricks on them. Eventually, Yuuta decides to unlock the secrets to why Earth will be destroyed and tries to save it! ",
                      type=TV[0],
                      category=ANIME[0])
    punchline.episode_counts = 0
    punchline.season = spring

    punchline_episode = Episode("Punch Line", "Punch Line", 1)
    punchline_episode.video = punchline
    _.db.add(punchline_episode)

    nisekoi = Video("Nisekoi: ", "Comedy, Romance, School, Shounen, Harem",
                    synopsis="Raku and the girls are back! The hunt for the key to his heart and locket continues in the second season of this fan favorite anime series. Nisekoi: features all the familiar characters from the first season joined by Kosaki's younger sister Haru. With a new girl entering the equation, will it really be 'more the merrier' for Raku? What will happen to this false love?",
                    type=TV[0],
                    category=ANIME[0])
    nisekoi.episode_counts = 12
    nisekoi.season = spring

    nisekoi_episode = Episode("From Now On / Please Notice", "Nisekoi:", 1,
                              "Acknowledging her love for Raku, Chitoge contemplates on how their faked relationship will progress from now on. Raku reveals to Chitoge, Kosaki and Marika that his locket has been returned to him but is still not completely repaired, preventing them from discovering the girl Raku made a promise with in the past. As Chitoge ruminates on the possibility of not being Raku's promised girl, the latter takes notice on Chitoge's anxiousness and assumes it as hunger for being on a diet, much to Chitoge's chagrin. In hopes to get Raku's attention, Chitoge makes constant refurbishes to her appearance which Raku constantly fails to notice, much to her vexation. Raku eventually reveals that he was aware of Chitoge's efforts yet refused to comment about it out of embarrassment though was not able able to notice Chitoge's new ribbon until it was pointed out to him by the latter, much to his surprise")
    nisekoi_episode.video = nisekoi
    _.db.add(nisekoi_episode)


    winter = season_qry.filter(Season.slug == "anime-winter-2015").first()


    deathparade = Video("Death Parade", "Mystery, Game, Psychological",
                        synopsis="After death, humans are either sent to\
                                       the void or reincarnated. But for some, at the instant of their death, they arrive at Quindecim, a bar attended by the mysterious white-haired Decim. He challenges them to the Death Game, wherein they wager their lives and reveal their true natures. Decim himself is the ultimate arbitrator of who wins and who loses, who will go to the void, and who will be reincarnated.",
                        type=TV[0],
                        category=ANIME[0])
    deathparade.episode_counts = 12
    deathparade.season = winter

    deathparade_episode = Episode("Death: Seven Darts", "Death Parade", 1,
                                  "Newlyweds Takashi and Machiko find themselves at the Quindecim bar, where the bartender, Decim, has them stake their lives in a game of darts, where each dart landed causes their partner great pain. As the game progresses, Takashi suspects that Machiko had been having an affair and tries to bend the match in his favor, only for Machiko to state this wasn't true at all, landing the winning hit. At the end of the game, it is revealed they had both died in a car crash because of Takashi's jealousy, with Machiko subsequently claiming she only married Takashi for his money. After Decim prevents Takashi from further attacking Machiko, he sends them to the elevators, where Takashi gets reincarnated and Machiko gets sent to the void. ")
    deathparade_episode.video = deathparade
    _.db.add(deathparade_episode)

    ansatsu = Video("Assasination Class", "Action, Comedy, School Life, Shounen",
                    synopsis=u'The story is about class 3-E of '
                             u'Kunugigaoka Middle School where every morning they'
                             u' greet their sensei with a massive firing squad.'
                             u' The sensei is a weird combination of an alien '
                             u'and a octopus that moves at speeds of mach-20. '
                             u'It turns out this creature was responsible for'
                             u' the destruction of the moon, rendering it forever'
                             u' in a crescent shape. He has announced that he will '
                             u'destroy the world in one year. The creature will teach '
                             u'class 3-E how to assassinate him before the year is over.',
                    type=TV[0],
                    category=ANIME[0])
    ansatsu.episode_counts = 22
    ansatsu.season = winter

    ansatsu_episode = Episode("Assasination Time", "Assasination Class", 1,
                              "In the March of a certain year a mysterious tentacled \
                              creature of unknown origin destroys over 70% of the moon, \
                              announcing that he will destroy the world in the same manner in one year. \
                              After several failed assassination attempts to kill him due to his Mach 20 speed, \
                              the creature makes a deal with the goverment to make him the teacher of Kunugigaoka \
                              Junior High School's Class 3-E, who are given specially designed weapons that can hurt \
                              the creature and offered a 10 billion yen reward to whoever can assassinate him\
                               before graduation. Although the students are generally frustrated with their failed\
                                assassination attempts, they discover the creature to be a respectable teacher in\
                                 his own right. A group of students involve Nagisa Shiota, a boy with not much self\
                                  worth, in their plan, in which they pin a grenade filled with creature-killing\
                                   pellets to him and detonate it within range. However, at that moment,\
                                    the creature sheds his skin, protecting both himself and Nagisa from the blast,\
                                     threatening the other students not to use any more plans that harm others\
                                      whilst also admiring Nagisa's efforts. To match their teacher's seemingly\
                                       unkillable nature, classmate Kaede Kayano gives the creature the fitting\
                                        name of Koro-sensei")
    ansatsu_episode.video = ansatsu
    _.db.add(ansatsu_episode)