/**
 * Copyright (c) 06 2015 | surya
 * 10/06/15 nanang.ask@kubuskotak.com
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 *  series.js
 */
/** jshint node: true */
"use strict";

var series = [
    {
        "_id" : ObjectId("555b5f9a4291f09b9be051c0"),
        "manga_url" : "http://m.mangahere.co/manga/nisekoi_komi_naoshi/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 2,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/8945/thumb_cover.jpg?v=1433747135",
        "slug" : "nisekoi-komi-na",
        "genres" : "Shounen, Comedy",
        "name" : "Nisekoi (KOMI Na...",
        "author" : "Komi Naoshi",
        "last_ch_name" : "Ch173",
        "last_date" : ISODate("2015-06-09T03:51:23.257Z"),
        "last_ch_chapter" : "nisekoi-komi-na-chapter-173"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051c3"),
        "manga_url" : "http://m.mangahere.co/manga/horimiya/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 3,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/11715/thumb_cover.jpg?v=1432891520",
        "slug" : "horimiya",
        "genres" : "Shounen, Comedy",
        "name" : "Horimiya",
        "author" : "HERO",
        "last_ch_name" : "Ch51",
        "last_date" : ISODate("2015-06-09T03:51:23.258Z"),
        "last_ch_chapter" : "horimiya-chapter-051"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051c2"),
        "manga_url" : "http://m.mangahere.co/manga/akame_ga_kiru/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 4,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/9229/thumb_cover.jpg?v=1432695988",
        "slug" : "akame-ga-kiru",
        "genres" : "Shounen, Action",
        "name" : "Akame ga Kiru!",
        "author" : "Takahiro",
        "last_ch_name" : "Ch60",
        "last_date" : ISODate("2015-06-09T03:51:23.259Z"),
        "last_ch_chapter" : "akame-ga-kiru-chapter-060"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051c1"),
        "manga_url" : "http://m.mangahere.co/manga/fairy_tail/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 5,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/246/thumb_cover.jpg?v=1433812925",
        "slug" : "fairy-tail",
        "genres" : "Shounen, Action",
        "name" : "Fairy Tail",
        "author" : "MASHIMA Hiro",
        "last_ch_name" : "Ch439",
        "last_date" : ISODate("2015-06-09T03:51:23.259Z"),
        "last_ch_chapter" : "fairy-tail-chapter-439"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051c4"),
        "manga_url" : "http://m.mangahere.co/manga/the_gamer/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 6,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/13739/thumb_cover.jpg?v=1431656763",
        "slug" : "the-gamer",
        "genres" : "Shounen, Action",
        "name" : "The Gamer",
        "author" : "Sung San-Young",
        "last_ch_name" : "Ch86.5",
        "last_date" : ISODate("2015-06-09T03:51:23.260Z"),
        "last_ch_chapter" : "the-gamer-chapter-86-5"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051c5"),
        "manga_url" : "http://m.mangahere.co/manga/minamoto_kun_monogatari/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 7,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/10005/thumb_cover.jpg?v=1433670722",
        "slug" : "minamoto-kun-mon",
        "genres" : "Comedy, Ecchi",
        "name" : "Minamoto-kun Mon...",
        "author" : "INABA Minori",
        "last_ch_name" : "Ch165",
        "last_date" : ISODate("2015-06-09T03:51:23.261Z"),
        "last_ch_chapter" : "minamoto-kun-mon-chapter-165"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051ca"),
        "manga_url" : "http://m.mangahere.co/manga/tate_no_yuusha_no_nariagari/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 8,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/15063/thumb_cover.jpg?v=1431654136",
        "slug" : "tate-no-yuusha-n",
        "genres" : "Action, Adventure",
        "name" : "Tate no Yuusha n...",
        "author" : "ANEKO Yusagi",
        "last_ch_name" : "Ch14",
        "last_date" : ISODate("2015-06-09T03:51:23.261Z"),
        "last_ch_chapter" : "tate-no-yuusha-n-chapter-014"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051c7"),
        "manga_url" : "http://m.mangahere.co/manga/yamada_kun_to_7_nin_no_majo/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 9,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/10642/thumb_cover.jpg?v=1433305503",
        "slug" : "yamada-kun-to-7",
        "genres" : "Shounen, Comedy",
        "name" : "Yamada-kun to 7-...",
        "author" : "YOSHIKAWA Miki",
        "last_ch_name" : "Ch161",
        "last_date" : ISODate("2015-06-09T03:51:23.262Z"),
        "last_ch_chapter" : "yamada-kun-to-7-chapter-161"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051c9"),
        "manga_url" : "http://m.mangahere.co/manga/girl_the_wild_s/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 10,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/9816/thumb_cover.jpg?v=1433605923",
        "slug" : "girl-the-wilds",
        "genres" : "Shounen, Action",
        "name" : "Girl the Wild's",
        "author" : "Hun",
        "last_ch_name" : "Ch191",
        "last_date" : ISODate("2015-06-09T03:51:23.262Z"),
        "last_ch_chapter" : "girl-the-wilds-chapter-191"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051c8"),
        "manga_url" : "http://m.mangahere.co/manga/onepunch_man/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 11,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/11912/thumb_cover.jpg?v=1433726402",
        "slug" : "onepunch-man",
        "genres" : "Action, Comedy",
        "name" : "Onepunch-Man",
        "author" : "ONE",
        "last_ch_name" : "Ch48",
        "last_date" : ISODate("2015-06-09T03:51:23.263Z"),
        "last_ch_chapter" : "onepunch-man-chapter-048"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051ce"),
        "manga_url" : "http://m.mangahere.co/manga/monster_musume_no_iru_nichijou/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 12,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/11110/thumb_cover.jpg?v=1432689615",
        "slug" : "monster-musume-n",
        "genres" : "Comedy, Ecchi",
        "name" : "Monster Musume n...",
        "author" : "Okayado",
        "last_ch_name" : "Ch33",
        "last_date" : ISODate("2015-06-09T03:51:23.264Z"),
        "last_ch_chapter" : "monster-musume-n-chapter-033"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051c6"),
        "manga_url" : "http://m.mangahere.co/manga/the_breaker_new_waves/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 13,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/8490/thumb_cover.jpg?v=1431658024",
        "slug" : "the-breaker-new",
        "genres" : "Shounen, Action",
        "name" : "The Breaker: New...",
        "author" : "JEON Geuk-jin",
        "last_ch_name" : "Ch201.5",
        "last_date" : ISODate("2015-06-09T03:51:23.265Z"),
        "last_ch_chapter" : "the-breaker-new-chapter-201-5"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051cb"),
        "manga_url" : "http://m.mangahere.co/manga/dungeon_ni_deai_o_motomeru_no_wa_machigatte_iru_darou_ka/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 14,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/13613/thumb_cover.jpg?v=1433728876",
        "slug" : "dungeon-ni-deai",
        "genres" : "Action, Adventure",
        "name" : "Dungeon ni Deai...",
        "author" : "OOMORI Fujino",
        "last_ch_name" : "Ch36",
        "last_date" : ISODate("2015-06-09T03:51:23.265Z"),
        "last_ch_chapter" : "dungeon-ni-deai-chapter-036"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051cd"),
        "manga_url" : "http://m.mangahere.co/manga/uq_holder/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 15,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/13688/thumb_cover.jpg?v=1433305622",
        "slug" : "uq-holder",
        "genres" : "Shounen, Action",
        "name" : "UQ Holder!",
        "author" : "AKAMATSU Ken",
        "last_ch_name" : "Ch81",
        "last_date" : ISODate("2015-06-09T03:51:23.266Z"),
        "last_ch_chapter" : "uq-holder-chapter-081"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051cc"),
        "manga_url" : "http://m.mangahere.co/manga/ao_no_exorcist/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 16,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/5646/thumb_cover.jpg?v=1430298183",
        "slug" : "ao-no-exorcist",
        "genres" : "Shounen, Action",
        "name" : "Ao no Exorcist",
        "author" : "KATOU Kazue",
        "last_ch_name" : "Ch67",
        "last_date" : ISODate("2015-05-26T20:05:17.103Z"),
        "last_ch_chapter" : "ao-no-exorcist-chapter-067"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051cf"),
        "manga_url" : "http://m.mangahere.co/manga/dragons_rioting/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 16,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/12661/thumb_cover.jpg?v=1422946921",
        "slug" : "dragons-rioting",
        "genres" : "Shounen, Action",
        "name" : "Dragons Rioting",
        "author" : "WATANABE Tsuyoshi",
        "last_ch_name" : "Ch22",
        "last_date" : ISODate("2015-06-09T03:51:23.266Z"),
        "last_ch_chapter" : "dragons-rioting-chapter-022"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051d0"),
        "manga_url" : "http://m.mangahere.co/manga/magi/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 17,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/6151/thumb_cover.jpg?v=1432796124",
        "slug" : "magi",
        "genres" : "Shounen, Action",
        "name" : "Magi",
        "author" : "OHTAKA Shinobu",
        "last_ch_name" : "Ch267",
        "last_date" : ISODate("2015-06-09T03:51:23.267Z"),
        "last_ch_chapter" : "magi-chapter-267"
    },


    {
        "_id" : ObjectId("555da2f44291f09b9be05b62"),
        "manga_url" : "http://m.mangahere.co/manga/ansatsu_kyoushitsu/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 18,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/11316/thumb_cover.jpg?v=1433726283",
        "slug" : "ansatsu-kyoushit",
        "genres" : "Shounen, Action",
        "name" : "Ansatsu Kyoushit...",
        "author" : "MATSUI Yuusei",
        "last_ch_name" : "Ch142",
        "last_date" : ISODate("2015-06-09T03:51:23.268Z"),
        "last_ch_chapter" : "ansatsu-kyoushit-chapter-142"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051d1"),
        "manga_url" : "http://m.mangahere.co/manga/noragami/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 19,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/9205/thumb_cover.jpg?v=1433728948",
        "slug" : "noragami",
        "genres" : "Shounen, Action",
        "name" : "Noragami",
        "author" : "ADACHI Toka",
        "last_ch_name" : "Ch55",
        "last_date" : ISODate("2015-06-09T03:51:23.268Z"),
        "last_ch_chapter" : "noragami-chapter-055"
    },

    {
        "_id" : ObjectId("555b5f9a4291f09b9be051d2"),
        "manga_url" : "http://m.mangahere.co/manga/to_love_ru_darkness/",
        "status" : "On going",
        "description" : "",
        "tags" : [],
        "rank" : 20,
        "chapters" : [],
        "thumb_url" : "http://a.mhcdn.net/store/manga/8471/thumb_cover.jpg?v=1432648323",
        "slug" : "to-love-ru-darkn",
        "genres" : "Shounen, Comedy",
        "name" : "To Love Ru Darkn...",
        "author" : "Hasemi Saki",
        "last_ch_name" : "Ch55",
        "last_date" : ISODate("2015-05-27T08:48:53.474Z"),
        "last_ch_chapter" : "to-love-ru-darkn-chapter-055"
    }];

exports.getAll = function () {
    return series;
}