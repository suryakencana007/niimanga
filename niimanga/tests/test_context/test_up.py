"""
 # Copyright (c) 03 2015 | surya
 # 11/03/15 nanang.ask@kubuskotak.com
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
 #  test_up.py
"""
from nose.tools import ok_, eq_
from niimanga.models import DBSession
from niimanga.models.auth import User
from niimanga.tests import TestDBBase
from niimanga.models.manga import Genre, Manga, Chapter, Author
import transaction


class TestCtx(TestDBBase):

    def test_insert_form(self):
        user = User.query\
            .filter(User.email == u'nanang999.ask@gmail.com')\
            .first()
        print(user.form[0].owner[0].id)
        eq_(12, user.id, "ok the go on")

    def test_init_manga(self):
        manga = Manga(u'Skip Beat!', 2006)
        manga.alt = u'Skip Beat!'
        manga.description = u'It is the story of Kyoko Mogami (Mogami Kyoko) a 16-year-old girl \
        who discovers that her childhood friend and romantic goal, Sho Fuwa, only keeps her around to act\
         as a maid and earn his living expenses, as he works his way to become the top pop idol in Japan...'
        DBSession.db.add(manga)

        manga.genre.append(self.find_genre(u'Comedy'))
        manga.genre.append(self.find_genre(u'Drama'))
        manga.genre.append(self.find_genre(u'Romance'))
        manga.genre.append(self.find_genre(u'Shoujo'))

        manga.author.append(self.find_author(u'Nakamura Yoshiki'))
        # request.db.add(manga)
        transaction.commit()

        manga = Manga(u'Fairy tail', 2006)
        manga.alt = u'Ekor Peri; Fairy Tail;'
        manga.description = u'A young celestial mage, Lucy Heartfilia,\
         runs away from home and travels to the land of Fiore to join\
          the magical Fairy Tail Guild. Along the way,\
           she meets Natsu Dragneel, a teenage boy looking for his foster parent,\
            a dragon named Igneel, with his best friend, Happy the cat. Shortly after their meeting,\
             Lucy is abducted by Bora of Prominence, who was posing as Salamander of Fairy Tail, to be sold as a slave.\
              Natsu rescues her and reveals that he is the real Salamander of fairy tail and has the skills of a Dragon Slayer,\
               an ancient fire magic. He offers her membership into the guild, which she gladly accepts, they along with\
                Erza Scarlet -Armored maiden, Gray Fullbuster -Ice Maker, and Happy become a team performing various\
                 missions offered to the Fairy Tail guild. Fairy Tail won the 2009 Kodansha Manga Award for shounen manga.\
                  It has also won The Society for the Promotion of Japanese Animation \'s Industry Awards for best comedy manga.'
        DBSession.add(manga)

        manga.genre.append(self.find_genre(u'Comedy'))
        manga.genre.append(self.find_genre(u'Drama'))
        manga.genre.append(self.find_genre(u'Action'))
        manga.genre.append(self.find_genre(u'Shounen'))
        manga.genre.append(self.find_genre(u'Fantasy'))
        manga.genre.append(self.find_genre(u'Adventure'))
        manga.genre.append(self.find_genre(u'Ecchi'))

        manga.author.append(self.find_author(u'Mashima Hiro'))
        # request.db.add(manga)
        transaction.commit()

        manga = Manga(u'Nanatsu no taizai', 2012)
        manga.alt = u'Nanatsu no Daizai; The Seven Deadly Sins;'
        manga.description = u'The "Seven Deadly Sins", a group of evil knights who\
         conspired to overthrow the kingdom of Britannia, were said to have been eradicated by the Holy Knights,\
          although some claim that they still live. Ten years later, the Holy Knights have staged a Coup d\'etat and\
           assassinated the king, becoming the new, tyrannical rulers of the kingdom. Elizabeth, daughter of the king,\
            sets out on a journey to find the "Seven Deadly Sins", and to enlist their help in taking back the kingdom.'
        DBSession.add(manga)

        manga.genre.append(self.find_genre(u'Comedy'))
        manga.genre.append(self.find_genre(u'Drama'))
        manga.genre.append(self.find_genre(u'Action'))
        manga.genre.append(self.find_genre(u'Shounen'))
        manga.genre.append(self.find_genre(u'Fantasy'))
        manga.genre.append(self.find_genre(u'Adventure'))
        manga.genre.append(self.find_genre(u'Ecchi'))

        manga.author.append(self.find_author(u'Suzuki Nakaba'))
        # request.db.add(manga)
        transaction.commit()

    def test_init_genre(self):
        genre = Genre()
        genre.name = u'Adventure'
        genre.slug = u'Adventure'
        genre.description = u''
        DBSession.add(genre)

        genre = Genre()
        genre.name = u'Comedy'
        genre.slug = u'Comedy'
        genre.description = u''
        DBSession.add(genre)

        genre = Genre()
        genre.name = u'Drama'
        genre.slug = u'Drama'
        genre.description = u''
        DBSession.add(genre)

        genre = Genre()
        genre.name = u'Fantasy'
        genre.slug = u'Fantasy'
        genre.description = u''
        DBSession.add(genre)

        genre = Genre()
        genre.name = u'School Life'
        genre.slug = u'School Life'
        genre.description = u''
        DBSession.add(genre)

        genre = Genre()
        genre.name = u'Shounen'
        genre.slug = u'Shounen'
        genre.description = u'Komik Shounen biasanya dibintangi oleh tokoh utama pria. Tema untuk ceritanya kebanyakan aksi atau petualangan.\
         Komik ini dibuat khusus untuk anak laki-laki\
Contoh untuk manga shounen adalah Naruto dan Bleach.'
        DBSession.add(genre)

        genre = Genre()
        genre.name = u'Seinen'
        genre.slug = u'Seinen'
        genre.description = u'Jika komik shounen ditujukan untuk\
         anak laki-laki, komik seinen ditujukan untuk pria dewasa.\
          Tema cerita komik seinen sendiri hampir sama dengan shounen namun lebih kasar dan vulgar.\
        Contoh untuk manga shounen adalah Berserk (TS belum pernah baca).'
        DBSession.add(genre)

        genre = Genre()
        genre.name = u'Shoujo'
        genre.slug = u'Shoujo'
        genre.description = u'Tadi sudah ada Shounen dan Seinen yang khusus pria,\
         manga Shoujo ini dikhususkan untuk anak perempuan.\
         Tokoh utamanya biasanya gadis remaja dengan konflik percintaan.\
         Ceritanya seputar percintaan dan ringan dikonsumsi.\
        Contoh untuk manga shounen adalah Electric Daisy.'
        DBSession.add(genre)

        genre = Genre()
        genre.name = u'Josei'
        genre.slug = u'Josei'
        genre.description = u'Manga Josei adalah manga khusus wanita dewasa.\
         Tema cerita komik josei sama dengan shoujo tapi\
          dengan cerita yang lebih rumit dan romantis.\
            Contoh untuk manga josei adalah Hana Yori Dango.'
        DBSession.add(genre)

        genre = Genre()
        genre.name = u'Kodomo'
        genre.slug = u'Kodomo'
        genre.description = u'Dari namanya sudah menunjukkan bahwa manga ini khusus anak-anak kecil (kodomo=anak kecil).\
         Tokoh utamanya adalah anak kecil dengan tema petualangan.\
        Contoh untuk manga shounen adalah Arale'
        DBSession.add(genre)

        genre = Genre()
        genre.name = u'Mecha'
        genre.slug = u'Mecha'
        genre.description = u'Sepertinya mecha ini diambil dari kata mechanic.\
         Tokoh utamanya bisa manusia atau robot dengan tema cerita pastinya seputar robot.\
            Contoh untuk manga shounen adalah Gundam.'
        DBSession.add(genre)
      

        genre = Genre()
        genre.name = u'Jidaegeki'
        genre.slug = u'Jidaegeki'
        genre.description = u'Manga ini mengambil\
         latar belakang masa lalu atau bercerita tentang sejarah.\
            Contoh untuk manga shounen adalah Samurai-X.'
        DBSession.add(genre)

        genre = Genre()
        genre.name = u'Ecchi'
        genre.slug = u'Ecchi'
        genre.description = u'Manga ini termasuk BB, \
        vulgar namun masih bisa dikonsumsi oleh remaja.\
        Contoh untuk manga ecchi adalah Fairy Tail\
        walaupun masih terdapat perbedaan pendapat mengenai penggolongan Fairy Tail ini ke dalam ecchi.'
        DBSession.add(genre)

        genre = Genre()
        genre.name = u'Harrem'
        genre.slug = u'Harrem'
        genre.description = u'manga jenis yang ini biasanya\
         ceritanya lebih dari echi tapi ga sampai kayak hentai.\
          biasanya manga jenis ini ada yang oneshoot ada yang series\
            contohnya : nozoki ana( recomended ), sun ken rock (harrem ama martial art ini gan ini juga ane recomended buat di baca)'
        DBSession.add(genre)

        genre = Genre()
        genre.name = u'Sifi'
        genre.slug = u'Sifi'
        genre.description = u'ini manganya ambil temanya science gitu gan.' \
                            u'tentang ilmu pengetahuan, masa depan, teknologi ya gitu deh' \
                            u'contohnya: hungry joker'
        DBSession.add(genre)

        genre = Genre()
        genre.name = u'Hentai'
        genre.slug = u'Hentai'
        genre.description = u''
        DBSession.add(genre)

    def test_init_chapter(self):
        manga = Manga.query.filter(Manga.slug == u'skip-beat').first()
        chapter = Chapter(u'Act. 1', 001)
        chapter.manga = manga

        mangar = Manga.query.filter(Manga.slug == u'skip-beat').first()
        chapter = Chapter(u'Act. 2', mangar.title, 001)
        chapter.manga = mangar

        # manga = Manga.query\
        #     .filter(Manga.slug == u'historys-strongest-disciple-kenichi')\
        #     .first()
        # manga = Manga(u'Historys Strongest Disciple Kenichi', 1998,
        #               genres="Comedy, Drama, Action, Fantasy, Harrem, Martial Arts, Shounen")
        # manga.alt = u'historys Strongest Disciple Kenichi;'
        # manga.description = u'The "historys Strongest Disciple Kenichi", a group of evil knights who\
        # conspired to overthrow the kingdom of Britannia, were said to have been eradicated by the Holy Knights,\
        #   although some claim that they still live. Ten years later, the Holy Knights have staged a Coup d\'etat and\
        #    assassinated the king, becoming the new, tyrannical rulers of the kingdom. Elizabeth, daughter of the king,\
        #     sets out on a journey to find the "Seven Deadly Sins", and to enlist their help in taking back the kingdom.'
        # # manga.set_genres()
        # manga.set_authors("Matsuena Syun")
        # DBSession.delete(manga)

        DBSession.add(chapter)

    def find_genre(self, keys):
        genre = Genre.query.filter(Genre.name == keys).first()

        if genre:
            return genre
        genre = Genre()
        genre.name = keys
        genre.slug = keys
        genre.description = u''
        return genre

    def find_author(self, keys):
        author = Author.query.filter(Author.name == keys).first()

        if author:
            return author
        author = Author()
        author.name = keys
        author.slug = keys

        return author