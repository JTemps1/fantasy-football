from statistics import mean
#Access data:

import requests
from getpass import getpass

fpl_data = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/').json()

for i, player in enumerate(fpl_data['elements']):
    
    fpl_data['elements'][i]['history'] = requests.get('https://fantasy.premierleague.com/api/element-summary/'
                                                             + str(player['id']) + '/').json()

'''
team_data = requests.get('https://fantasy.premierleague.com/api/my-team/1547766/', 
                         auth = ('jtemps@live.co.uk', getpass())).json()
'''
#Function to determine form in different aspects for the last 5 games:
def player_form_calculator(elements, x):
    i = len(elements)
    k = 1
    goals, assists, cleansheet, bonus, minutes, saves, reds, yellows = [],[],[],[],[],[],[],[]
    if x == 'goal_form':
        while k <= 5 and k <= i:
            goals += [elements[(i-k)]['goals_scored']]
            k += 1
        return mean(goals)
        
    elif x == 'assist_form':
        while k <= 5 and k <= i:
            assists += [elements[(i-k)]['assists']]
            k += 1
        return mean(assists)
    
    elif x == 'cleansheet_form':
        while k <= 5 and k <= i:
            cleansheet += [elements[(i-k)]['clean_sheets']]
            k += 1
        return mean(cleansheet)
    
    elif x == 'bonus_form':
        while k <= 5 and k <= i:
            bonus += [elements[(i-k)]['bonus']]
            k += 1
        return mean(bonus)
    
    elif x == 'minutes_form':
        while k <= 5 and k <= i:
            minutes += [elements[(i-k)]['minutes']]
            k += 1
        return mean(minutes)/90
    
    elif x == 'saves_form':
        while k <= 5 and k <= i:
            saves += [elements[(i-k)]['saves']]
            k += 1
        return mean(saves)
    
    elif x == 'red_card_form':
        while k <= 5 and k <= i:
            reds += [elements[(i-k)]['red_cards']]
            k += 1
        return mean(reds)
    
    elif x == 'yellow_card_form':
        while k <= 5 and k <= i:
            yellows += [elements[(i-k)]['yellow_cards']]
            k += 1
        return mean(yellows)
    
    else:
        return 0

#Simple program to calculate the average difficulty of upcoming fixtures:
def fixture_average(fixts):
    i = len(fixts)
    k = 0
    fixtures = []
    while k < 5 and k <= i:
        fixtures += [fixts[k]['difficulty']]
        k += 1
    return mean(fixtures)

#Simple function to convert position into a more user friendly format:
def positioner(x):
    if x == 1:
        return 'GK'
    elif x == 2:
        return 'DEF'
    elif x == 3:
        return 'MID'
    elif x == 4:
        return 'ATT'
    

#Define Player as a class, each object will contain all relevant information about a player:
class Player:
    
    def __init__(self, team, info):
        
        self.name = info['first_name'] + ' ' + info['second_name']
        self.team = team['name']
        self.position = positioner(info['element_type'])
        self.gc = info['goals_scored'] / len(info['history']['history'])
        self.gf = player_form_calculator(info['history']['history'], 'goal_form')
        self.ac = info['assists'] / len(info['history']['history'])
        self.af = player_form_calculator(info['history']['history'], 'assist_form')
        self.csc = info['clean_sheets'] / len(info['history']['history'])
        self.csf = player_form_calculator(info['history']['history'], 'cleansheet_form')
        self.bpc = info['bonus'] / len(info['history']['history'])
        self.bpf = player_form_calculator(info['history']['history'], 'bonus_form')
        self.mpf = player_form_calculator(info['history']['history'], 'minutes_form')
        self.svc = info['saves'] / len(info['history']['history'])
        self.svf = player_form_calculator(info['history']['history'], 'saves_form')
        self.rcc = info['red_cards'] / len(info['history']['history'])
        self.rcf = player_form_calculator(info['history']['history'], 'red_card_form')
        self.ycc = info['yellow_cards'] / len(info['history']['history'])
        self.ycf = player_form_calculator(info['history']['history'], 'yellow_card_form')
        self.tf = 0
        self.tc = 0
        self.fixtures = fixture_average(info['history']['fixtures'])
        self.form = 0
        
    def player_form(self):
        if self.position == 'GK':
            a,b,c,d,e,f,g,h,i,j = 6,3,4,1,(-1),1,1,1/3,(-3),(-1)
            
            F = ((a*(self.gc) + 2*a*(self.gf) + b*(self.ac) + 2*b*(self.af) + c*(self.csc) + 2*c*(self.csf) +
                 d*(self.bpc) + 2*d*(self.bpf) + e*(self.fixtures) + f*(self.mpf) + g*(self.tc) + 2*g*(self.tf) +
                 h*(self.svc) + 2*h*(self.svf) + i*(self.rcc) + 2*i*(self.rcf) + j*(self.ycc) + 2*j*(self.ycf))
                 / abs(3*a + 3*b + 3*c + 3*d + e + f + 3*g + 3*h + 3*i + 3*j))
            
            self.form = F
            return F
            
        elif self.position == 'DEF':
            a,b,c,d,e,f,g,h,i,j = 6,3,4,1,(-2),2,1,1/3,(-3),(-1)
            
            F = ((a*(self.gc) + 2*a*(self.gf) + b*(self.ac) + 2*b*(self.af) + c*(self.csc) + 2*c*(self.csf) +
                 d*(self.bpc) + 2*d*(self.bpf) + e*(self.fixtures) + f*(self.mpf) + g*(self.tc) + 2*g*(self.tf) +
                 h*(self.svc) + 2*h*(self.svf) + i*(self.rcc) + 2*i*(self.rcf) + j*(self.ycc) + 2*j*(self.ycf))
                 / abs(3*a + 3*b + 3*c + 3*d + e + f + 3*g + 3*h + 3*i + 3*j))
            
            self.form = F
            return F
            
        elif self.position == 'MID':
            a,b,c,d,e,f,g,h,i,j = 5,3,1,1,(-2),2,1,1/3,(-3),(-1)
            
            F = ((a*(self.gc) + 2*a*(self.gf) + b*(self.ac) + 2*b*(self.af) + c*(self.csc) + 2*c*(self.csf) +
                 d*(self.bpc) + 2*d*(self.bpf) + e*(self.fixtures) + f*(self.mpf) + g*(self.tc) + 2*g*(self.tf) +
                 h*(self.svc) + 2*h*(self.svf) + i*(self.rcc) + 2*i*(self.rcf) + j*(self.ycc) + 2*j*(self.ycf))
                 / abs(3*a + 3*b + 3*c + 3*d + e + f + 3*g + 3*h + 3*i + 3*j))
            
            self.form = F
            return F
            
        elif self.position == 'ATT':
            a,b,c,d,e,f,g,h,i,j = 4,3,0,1,(-2),2,1,1/3,(-3),(-1)
            
            F = ((a*(self.gc) + 2*a*(self.gf) + b*(self.ac) + 2*b*(self.af) + c*(self.csc) + 2*c*(self.csf) +
                 d*(self.bpc) + 2*d*(self.bpf) + e*(self.fixtures) + f*(self.mpf) + g*(self.tc) + 2*g*(self.tf) +
                 h*(self.svc) + 2*h*(self.svf) + i*(self.rcc) + 2*i*(self.rcf) + j*(self.ycc) + 2*j*(self.ycf))
                 / abs(3*a + 3*b + 3*c + 3*d + e + f + 3*g + 3*h + 3*i + 3*j))
            
            self.form = F
            return F



allPlayers = []

for i in range(len(fpl_data['elements'])):
    
    team_index = fpl_data['elements'][i]['team'] - 1
    
    player = Player(fpl_data['teams'][team_index], fpl_data['elements'][i])
    
    allPlayers.append(player)

GK_form_index = []
DEF_form_index = []
MID_form_index = []
ATT_form_index = []

for n in allPlayers:
    if n.position == 'GK':
        GK_form_index.append([n.name, n.team, n.player_form()])
        
    elif n.position == 'DEF':
        DEF_form_index.append([n.name, n.team, n.player_form()])
        
    elif n.position == 'MID':
        MID_form_index.append([n.name, n.team, n.player_form()])
        
    elif n.position == 'ATT':
        ATT_form_index.append([n.name, n.team, n.player_form()])
        


GK_form_index.sort(key = lambda n: n[2], reverse = True)
DEF_form_index.sort(key = lambda n: n[2], reverse = True)
MID_form_index.sort(key = lambda n: n[2], reverse = True)
ATT_form_index.sort(key = lambda n: n[2], reverse = True)

print('\nThe most in-form goalkeepers are:\n')
for n in GK_form_index[:10]:
    print('{0:s}, {1:s}: {2:.3}'.format(n[0], n[1], n[2]))

print('\nThe most in-form defenders are:\n')
for n in DEF_form_index[:10]:
    print('{0:s}, {1:s}: {2:.3}'.format(n[0], n[1], n[2]))

print('\nThe most in-form midfielders are:\n')
for n in MID_form_index[:10]:
    print('{0:s}, {1:s}: {2:.3}'.format(n[0], n[1], n[2]))

print('\nThe most in-form attackers are:\n')
for n in ATT_form_index[:10]:
    print('{0:s}, {1:s}: {2:.3}'.format(n[0], n[1], n[2]))    

