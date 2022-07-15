from heroes import SuperHero, Superman
from mass_media import MassMedia, Newspapers
from places import Kostroma, Place, Tokyo


def save_the_place(hero: SuperHero, place: Place, media: MassMedia):
    hero.find(place)
    hero.attack()
    if hero.can_use_ultimate_attack:
        hero.ultimate()
    media.create_news(hero, place)


if __name__ == '__main__':
    media: MassMedia = Newspapers()
    save_the_place(Superman(), Kostroma(), media)
    print('-' * 20)
    save_the_place(SuperHero('Chack Norris', False), Tokyo(), media)
