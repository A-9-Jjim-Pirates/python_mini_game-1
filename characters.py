import random


class Character:
    """
    모든 캐릭터의 모체가 되는 클래스
    """

    def __init__(self, name, hp, power, magic_power, agility):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.power = power
        self.magic_power = magic_power
        self.agility = agility

    def attack(self, other):
        print(f'{self.name}이(가) {other.name}에게 공격!')

        damage = random.randint(int(self.power*0.8), int(self.power*1.2))
        print(f'{damage}의 데미지!')
        other.hp = max(other.hp - damage, 0)

    def check_status(self):
        return f"{self.hp} / {self.max_hp}"


class Hero(Character):
    def __init__(self, name, hp, power, magic_power, agility, mana):
        super().__init__(name, hp, power, magic_power, agility)
        self.max_mana = mana
        self.mana = mana
        self.level = 0
        self.mana_spend = 10

    def hero_mana_check(self):
        if self.mana-self.mana_spend >= 0:
            self.mana -= self.mana_spend
            return True
        else:
            return False

    def hero_magic_attack(self, other):
        if not self.hero_mana_check():
            print("아차! 마나가 부족합니다....공격실패!")
            return False
        damage = random.randint(int(self.magic_power*0.8),
                                int(self.magic_power*1.2))
        damage = max(damage-other.magic_power, 0)
        other.hp = max(other.hp - damage, 0)
        print(f'{self.name}이(가) {other.name}({other.monster_class_name})에게 마법 공격!')
        print(f'{damage}의 데미지!')
        return True

    def hero_check_status(self):
        return f"{self.hp} / {self.max_hp}", f"{self.mana} / {self.max_mana}"

    def hero_level_up(self):
        self.level += 1
        # self.max_hp += random.randint(10, 20)
        # self.power += random.randint(3, 5)
        # self.magic_power += random.randint(3, 5)
        # self.max_mana += random.randint(5, 15)
        # self.agility += random.randint(1, 3)
        self.max_hp += random.randint(100, 200)
        self.power += random.randint(30, 50)
        self.magic_power += random.randint(30, 50)
        self.max_mana += random.randint(50, 150)
        self.agility += random.randint(10, 30)


# 직업이랑 개네들 특수 능력 하기.
class Archer(Hero):     # 궁수
    def hero_magic_attack(self, other):  # other = 공격대상
        if not super().hero_magic_attack(other):
            return
        for i in range(2):
            if random.randint(1, 5+self.magic_power//5) >= 5:
                print(f'마법의 힘으로 화살이 복사됐다. {i+1}개!')
                self.attack(other)


class SwordMan(Hero):     # 전사 # 분기문 깔끔하게 바꿀것
    def hero_magic_attack(self, other):
        if not self.hero_mana_check():  # mana check 부분
            print("아차! 마나가 부족하다....공격실패!")
            return False
        dice = random.randint(1, 20)
        # 1-10까지 있는 주사위를 던졌을 때 나온 숫자와 '9-레벨'과 비교해서 크거나 같으면 스킬 발동되는것
        if dice >= max(18-self.level, 16):
            print(f' 즉살 검기를 목에 맞췄다!')
            other.hp = 0
            print(f' {other.name}즉사!')
            return
        if dice >= max(5-self.level, 2):  # 일반적인 마법 공격
            self.mana += self.mana_spend
            print(f'검기가 적의 목에서 살짝 빗나갔다!')
            super().hero_magic_attack(other)
        else:
            print(f'대 참사! 검기가 스스로를 베었다!')  # 자해
            damage = random.randint(int(self.magic_power*0.3),
                                    int(self.magic_power*0.8))
            print(f'{damage}의 데미지!')
            if self.hp-damage <= 5:
                print('다행히 아슬아슬하게 죽음은 면했다!')
            self.hp = max(5, self.hp-damage)


class Wizard(Hero):     # 마법사
    def hero_magic_attack(self, other: Character):
        if not super().hero_magic_attack(other):
            return
        if other.hp == 0:  # hp가 0이면
            return  # 실행하지 않는다
        if dice := random.randint(1, 6) >= 5:
            print(f'특수 효과 발동! 몬스터의 마법공격/저항이 약해졌다.')
            other.power = max(2, other.magic_power - (1+self.level))
        if dice > 2:
            print(f'특수 효과 발동! 몬스터의 힘이 약해졌다.')
            other.power = max(2, other.power - (1+self.level))


class Monster(Character):  # 몬스터
    def __init__(self, name, hp, power, magic_power, agility, monster_class_name):
        super().__init__(name, hp, power, magic_power, agility)
        self.monster_class_name = monster_class_name
        self.reward = random.randint(0, 100)


boss_names = ['Baal', 'Diablo', 'Rucifer', 'Haster']


class BossMonster(Monster):
    def __init__(self):
        self.name = random.choice(boss_names)
        boss_names.pop(boss_names.index(self.name))
        self.hp = 150
        self.max_hp = 350
        self.power = 15
        self.magic_power = 20
        self.agility = 19
        self.monster_class_name = "대악마"
        self.reward = 1000

    def attack(self, other):
        move_list = [super().attack,
                     super().attack,
                     self.magic_power_attack,
                     self.power_hp_drain,
                     self.mana_drain
                     ]
        move = random.choice(move_list)
        move(other)

    def magic_power_attack(self, other):
        total_power = self.magic_power+self.power
        damage = random.randint(int(total_power*0.8),
                                int(total_power*1.3))
        damage = max(damage-other.magic_power, 0)
        other.hp = max(other.hp - damage, 0)
        print(f'{self.name}이(가) {other.name}에게 마법(물리)공격!)')
        print(f'{damage}의 데미지!')
        return True

    def power_hp_drain(self, other):
        print(f'{self.name}이(가) {other.name}에게 흡혈 공격!')
        super().attack(other)
        self.hp = min(self.max_hp, self.hp+int(self.power * 0.5))
        print(f'{self.name}이(가) 체력을 {int(self.power * 0.5)}만큼 회복.')

    def mana_drain(self, other):
        print(f'{self.name}이(가) {other.name}에게 흡성대법공격!')
        other.mana = max(0, other.mana-self.magic_power)
        heal = int(self.magic_power * 0.3)
        magic_power_up = int(self.magic_power * 0.2)
        self.hp = min(self.max_hp, self.hp+heal)
        self.magic_power += magic_power_up
        print(f'{other.name}이(가) 마나를 {self.magic_power}만큼 잃었다')
        print(f'{self.name}이(가) 마나를 먹어 체력을 회복하고 마법력을 증가시켰다!')
