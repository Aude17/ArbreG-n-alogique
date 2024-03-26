# Reste :
# - Ameliorer les ecrans de l'application
# - Avoir plus de données pour la demonstration
# - Faire le stockage et la lecture de l'arbre sur disque

# Person class to represent a person and its children tree
class Person:
    def __init__(self, fname, lname, address, nationality, phone, birthday,fathername,fatherbirthday,motherfirstname,motherlastname,motherbirthday):
        self.firstname = fname
        self.lastname = lname
        self.address = address
        self.nationality = nationality
        self.phone=phone
        self.birthday=birthday
        self.fathername=fathername
        self.fatherbirthday= fatherbirthday
        self.motherfirstname=motherfirstname
        self.motherlastname=motherlastname
        self.motherbirthday= motherbirthday
        self.children = []
        self.mother = None
        self.father = None

    def attach_child(self, child):
        self.children.append(child)

    def detach_child(self, child):
        self.children.remove(child)

    def attach_mother(self, mother):
        self.mother=mother

    def attach_father(self, father):
        self.father=father

    def attached_children(self):
        return self.children
    
    # search the person and its attached childs for a matching : firstname,lastname, birthday (if not None)
    def search_tree(self,firstname,lastname,birthday,search_result):
        if self.firstname==firstname and self.lastname==lastname:
            if birthday==None or birthday==self.birthday:
                search_result.append(self)
        for child in self.children:
            child.search_tree(firstname,lastname,birthday,search_result)
        return
    
    # search the person and its attached childs for parent maching on  :
    #       fathername,motherfirstname, motherlastname, fatherbirthday (if not None), motherbirthday (if not None)
    def search_tree_by_parent(self,pfname,plname,pbirthday,search_result):
        if self.fathername==pfname and self.lastname==plname:
            if pbirthday==None or pbirthday==self.fatherbirthday:
                search_result.append(self)
        if self.motherfirstname==pfname and self.motherlastname==plname:
            if pbirthday==None or pbirthday==self.motherbirthday:
                search_result.append(self)
        for child in self.children:
            child.search_tree_by_parent(pfname,plname,pbirthday,search_result)
        return
    
    #  search all persons, in the curret person and its attached childs for person whitout attachment criteria : noparent, nochildren
    #       search is done in distincts (no resukts duplicates)
    def search_no_attachement(self,attach_type,search_result):
        if attach_type=='noparent' and self.mother==None and self.father==None:
            if self not in search_result:
                search_result.append(self)
        if attach_type=='nochildren' and (self.children==None or len(self.children)==0):
            if self not in search_result:
                search_result.append(self)
        for child in self.children:
            child.search_no_attachement(attach_type,search_result)
        return

    #  search all persons, in the current person and its attached childs for person with an attachment criteria : mother, father, children
    #       search is done in distincts (no resukts duplicates)
    def search_with_attachement(self,attach_type,search_result):
        if attach_type=='mother' and self.mother!=None:
            if self not in search_result:
                search_result.append(self)
        if attach_type=='father' and self.father!=None:
            if self not in search_result:
                search_result.append(self)
        if attach_type=='children' and (self.children!=None and len(self.children)>0):
            if self not in search_result:
                search_result.append(self)
        for child in self.children:
            child.search_with_attachement(attach_type,search_result)
        return
    
    # find the height of the longuest ascendant (fathers & mothers) path of current person
    def longest_parent_path(self):
        if self.father==None and self.mother==None:
            return 1
        if self.father!=None and self.mother!=None:
            return 1+ max(self.father.longest_parent_path(),self.mother.longest_parent_path())
        if self.father!=None:
            return 1+self.father.longest_parent_path()
        else: return 1+self.mother.longest_parent_path()

    # create a text representation of a person information (used automatically when calling print on a person object)
    def __str__(self):
        string =100*'-'+'\n'
        string +='>>> '+self.firstname+' '+self.lastname + "["+str(self.fathername)+","+str(self.motherfirstname)+" "+str(self.motherlastname)+"]"
        if self.father!=None:
            string +=' (Attached Father:'+self.father.firstname+')'
        else:
            string +=" (Attached Father: None)"
        if self.mother!=None:
            string +=" (Attached Mother:"+self.mother.firstname+' '+self.mother.lastname+')'
        else:
            string +=" (Attached Mother: None)"
        if self.children==None or len(self.children) ==0:
            string +=" (Children: None)"
        else:
            string +=" (Children:"
            for child in self.children:
                string +=child.firstname+' '+child.lastname+' ; '
            string +=")"
        return string
    
    # define equal operator on person object (used implicitly in all search features, specially tests : if person in list)
    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        return self.firstname==other.firstname and self.lastname==other.lastname and self.birthday==other.birthday

    # return current and all its descendant attached childs (distincts)
    def get_all_persons_distincts(self,result=[]):
        if self not in result:
            result.append(self)
        for child in self.children:
            child.get_all_persons_distincts(result)
    
    # print current and all its descendant attached childs (distincts)
    def display_tree(self):
        found = self.get_all_persons_distincts()
        for person in found:
            print(person)

    # print attached childs to current person
    def display_children(self):
        print('children of',self.firstname,self.lastname)
        for child in self.children:
            print(child)

    # print attached father and mother to current person
    def display_parents(self):
        print('Parents of',self.firstname,self.lastname)
        if self.father!=None:
            print('Father:',self.father)
        else: print('Father: None')
        if self.mother!=None:
            print('Mother:',self.mother)
        else: print('Mother: None')



# Trees class implements all family trees (any person not attached to existing tree is a new tree)
class Trees:
    def __init__(self):
        self.familytrees = []

    def add_family_tree(self,family_tree):
        self.familytrees.append(family_tree)

    # collect distincts person in the whole Genealogique data structure
    # il collect distincts persons of each family tree (by calling get_all_persons_distincts on its top person)
    def get_all_persons_distincts(self):
        all_found=[]
        for family in self.familytrees:
            found =[]
            family.get_all_persons_distincts(found)
            if len(found)>0:
                for person in found:
                    if person not in all_found:
                        all_found.append(person)
        return all_found
    
    # print distincts person in the whole Genealogique data structure
    def display(self):
        for person in self.get_all_persons_distincts():
            print(person)

    # search distinct persons matching (firstname,lastname,birthday) criteria in the whole Genealogique data structure
    # it is based on Person class search_tree() method
    def search_person(self,firstname,lastname,birthday=None):
        parent_proposition=[]
        for family in self.familytrees:
            found =[]
            family.search_tree(firstname,lastname,birthday,found)
            if len(found)>0:
                for person in found:
                    if person not in parent_proposition:
                        parent_proposition.append(person)
        return parent_proposition

    # search distinct persons matching parents(firstname,lastname,birthday) criteria in the whole Genealogique data structure
    # it is based on Person class search_tree_by_parent() method
    def search_person_by_parent(self,pfname,plname,pbirthday):
        child_proposition=[]
        for family in self.familytrees:
            found =[]
            family.search_tree_by_parent(pfname,plname,pbirthday,found)
            if len(found)>0:
                for person in found:
                    if person not in child_proposition:
                        child_proposition.append(person)
        return child_proposition
    
    # delete a person and its attachments (and attachments of others to him) from Genealogique data structure
    # it perform a full clean up of the person passed in parameter
    # his children get added as new family trees if they become orphalan
    def delete_person(self,person):
        print('deleting:',person.firstname,person.lastname)
        if person in self.familytrees:
            self.familytrees.remove(person)
        if person.father !=None:
            person.father.detach_child(person)
        if person.mother !=None:
            person.mother.detach_child(person)
        for child in person.attached_children():
            reattach = False
            if child.father==person:
                if child.mother==None:
                    reattach=True
            if child.mother==person:
                if child.father==None:
                    reattach=True
            if reattach:
                self.add_family_tree(child)
                child.father=child.mother=None
        person.father=None
        person.mother=None
        person.children=[]
        del person
        return True
    
    def get_nb_families(self):
        return len(self.familytrees)
    
    # similar to search_with_attachement of Person, but applied to all families trees
    def search_with_attachement(self,attach_type):
        all_found=[]
        for family in self.familytrees:
            found =[]
            family.search_with_attachement(attach_type,found)
            if len(found)>0:
                for person in found:
                    if person not in all_found:
                        all_found.append(person)
        return all_found

    # similar to search_no_attachement of Person, but applied to all families trees
    def search_no_attachement(self,attach_type):
        all_found=[]
        for family in self.familytrees:
            found =[]
            family.search_no_attachement(attach_type,found)
            if len(found)>0:
                for person in found:
                    if person not in all_found:
                        all_found.append(person)
        return all_found
    
    # find the person with the longest ascendant path
    # it collect all persons with parent attachment, 
    # then call longest_parent_path() on each each persons and find longest
    def persons_longest_parent_path(self):
        with_parent= self.search_with_attachement('father')
        for person in self.search_with_attachement('mother'):
            if person not in with_parent:
                with_parent.append(person)
        longest_path=0
        for person in with_parent:
            person_longest_path = person.longest_parent_path()
            if person_longest_path > longest_path:
                longest_path = person_longest_path
                person_longest = person
        return person_longest
          

# create a Person instance for a newly defined application user
# it proposes selecting parent attachment for the new person
# if not attachment done, the create person is added as a new family tree    
def create_person(trees):
    fname=input('votre prenom:')
    lname=input('votre nom:')
    address=input('adresse:')
    nationality=input('nationalité:')
    phone=input('telephone')
    birthday=input('date de naissance:')
    fathername=input('prenom du pere:')
    fatherbirthday=input('date de naissance du pere:')
    motherfirstname=input('prenom de la mere:')
    motherlastname=input('nom de la mere:')
    motherbirthday=input('date de naissance de la mere:') 

    person = Person(fname, lname, address, nationality, phone, birthday,fathername,fatherbirthday,motherfirstname,motherlastname,motherbirthday)

    if add_direct_parent(trees,person)==0:
        trees.add_family_tree(person)
    
    return person

# used to identify the application user in the Genealogique tree
# it is called on application startup, and propose to create the user
# of to find his node in case he is a recurrent user
def identify_persone(trees):
    isnew = input("vous etes deja inscrit dans l'arbre (o/n):")
    if isnew=='o':
        fname=input('votre prenom:')
        lname=input('votre nom:')
        birthday=input('date de naissance:')
        persone=trees.search_person(fname,lname,birthday)
        if persone:
            return persone[0]
        else: return None
    else :
        persone = create_person(trees)
        if persone:
            print('Inscription avec succes')
        return persone

###########################   M A I N   M E N U  complex Operations  ###########################

# Menu option 1
def add_direct_parent(trees,person):
    print('add_direct_parent')
    proposition_peres=trees.search_person(person.fathername,person.lastname,None)
    print('proposition_peres')
    proposition_meres=trees.search_person(person.motherfirstname,person.motherlastname,None)
    print('proposition_meres')
    choix1=choix2=0
    if proposition_peres:
        print('Proposition de pere')
        i=1
        for pere in proposition_peres:
            print(i,'-',pere.firstname,pere.lastname,pere.birthday)
            i+=1
        print("Choisir votre pere (0 pour rien):")
        choix1 = int(input('votre choix:'))
        if choix1!=0:
            person.attach_father(proposition_peres[choix1-1])

    if proposition_meres:
        print('Proposition de mere')
        i=1
        for mere in proposition_meres:
            print(i,'-',mere.firstname,mere.lastname,mere.birthday)
            i+=1
        print("Choisir votre mere (0 pour rien):")
        choix2 = int(input('votre choix:'))
        if choix2!=0:
            person.attach_mother(proposition_meres[choix2-1])

    if not proposition_meres and not proposition_meres:
        print("\n>>>>>>>>>>>>>Aucun attachement de parent est possible % a l'arbre actuel\n\n")
    return choix1+choix2  

# Menu option 2
def  add_person_child(trees,person):
    child_proposition=trees.search_person_by_parent(person.firstname,person.lastname,None)
    if child_proposition:
        print("Proposition d'enfants")
        i=1
        for child in child_proposition:
            print(i,'-',child.firstname,child.lastname,child.birthday)
            i+=1
        print("Choisir votre enfant (0 pour rien):")
        choix = int(input('votre choix:'))
        if choix!=0:
            person.attach_child(child_proposition[choix-1])
            print("\n>>>>>>>>>>>>>Attachement d'enfant reussite\n\n")
    else: 
        print("\n>>>>>>>>>>>>>Aucun attachement d'enfant est possible % a l'arbre actuel\n\n")

# Menu option 3
def delete_current_user(trees,current_user):
    if trees.delete_person(current_user):
        print("\n>>>>>>>>>>>>> Supression avec success \n\n")
    return       

# Menu option 4
def delete_direct_parent(trees,current_user):
    if current_user.father==None and current_user.mother==None:
        print("\n>>>>>>>>>>>>> Pas de parents definis pour faire une Supression\n\n")
        return
    if current_user.father!=None:
        print("Votre pere est:")
        print(current_user.father)
        choix=input('Voulez vous le supprimer (o/n)?')
        if choix=='o':
            current_user.father=None
            print("\n>>>>>>>>>>>>> Supression du pere avec success \n\n")
    if current_user.mother!=None:
        print("Votre mere est:")
        print(current_user.mother)
        choix=input('Voulez vous la supprimer (o/n)?')
        if choix=='o':
            current_user.mother=None
            print("\n>>>>>>>>>>>>> Supression du mere avec success \n\n")
    return   

# Menu option 5
def delete_children(trees,current_user):
    if current_user.attached_children()==None or len(current_user.attached_children())==0:
        print("\n>>>>>>>>>>>>> Pas d'enfants pour faire une Supression\n\n")
        return
    print('Vos enfants sont:')
    i=1
    for child in current_user.attached_children():
        print(i,'-',child)
        i+=1
    print("Choisir l'enfant a supprimer (0 pour rien):")
    choix = int(input('votre choix:'))
    if choix!=0 and choix<=len(current_user.attached_children()):
        print("\n>>>>>>>>>>>>> Supression de",current_user.attached_children()[choix-1],"avec success \n\n")
        current_user.attached_children().pop(choix-1)
    return   

# Menu option 11
def filter_by_attachment(trees):
    print('\t\t\t1- Afficher les personnes avec attachement de mere')
    print('\t\t\t2- Afficher les personnes avec attachement de pere')
    print("\t\t\t3- Afficher les personnes avec attachement d'enfants")
    print('\n\t\t(0- pour revenir)')
    choice = int(input('Donner le numero de votre choix:'))
    if choice <=0 or choice > 3:
        return
    if choice==1:
        found=trees.search_with_attachement('mother')
    elif choice==2:
        found=trees.search_with_attachement('father')
    else: found=trees.search_with_attachement('children')
    print('Personnes trouvées:')
    if len(found)>0:
        for person in found:
            print(person)
    else: print('Aucun')

# Menu option 12 - 13
def filter_no_attachment(trees,attachtype):
    found=trees.search_no_attachement(attachtype)
    print('Personnes trouvées:')
    if len(found)>0:
        for person in found:
            print(person)
    else: print('Aucun')

###########################  E N D      M A I N   M E N U  complex Operations  ###########################


def max(a,b):
    if a>b:
        return a
    else: return b


# create a sample Genealogical Tree for testing
def load_trees():
    trees = Trees()
    grandpere1 = Person("Jacques", "Dupont", "4 Rue de la Paix", "Française", "0924637825", "1960-11-23", None, None, None, None, None)
    grandmere1 = Person("Christine", "Dupont", "4 Rue de la Paix", "Française", "0198765432", "1962-01-30", None, None, None, None, None)
    pere1 = Person("Jean", "Dupont", "1 Rue de la Paix", "Française", "0123456789", "1980-05-10", "Jacques", "1960-11-23", "Christine", "Dupont", "1962-01-30")
    mere1 = Person("Marie", "Dupont", "1 Rue de la Paix", "Française", "0123456789", "1982-08-15", None, None, None, None, None)
    enfant1 = Person("Luc", "Dupont", "1 Rue de la Paix", "Française", "0123456789", "2005-02-20", "Jean", "1980-05-10", "Marie", "Dupont", "1982-08-15")

    # Création d'autres personnes pour tester les propositions
    pere2 = Person("Pierre", "Martin", "2 Rue de la Prose", "Française", "0643436728", "1975-04-25", None, None, None, None, None)
    mere2 = Person("Sophie", "Martin", "2 Rue de la Prose", "Française", "0698243618", "1978-07-30", None, None, None, None, None)
    enfant2 = Person("Emma", "Martin", "2 Rue de la Prose", "Française", "0647382910", "2002-11-15", "Pierre", "1975-04-25", "Sophie", "Martin", "1978-07-30")

    # Création d'autres personnes pour tester les propositions
    # lui ne s'affiche pas car pas attaché
    pere3 = Person("Francois", "Laurent", "4 rue de l'Eglise", "Française", "0638329218", "1975-04-25", None, None, None, None, None)
    enfant11 = Person("Audrey", "Dupont", "4 rue de l'Eglise", "Française", "0689372615", "1978-07-30", None, None, None, None, None)
    enfant3 = Person("Manon", "Dupont", "10 rue Antoine Hervet", "Française", "0743568214", "2002-11-15", None, None, None, None, None)

    # Ajout des personnes à l'arbre généalogique
    grandpere1.attach_child(pere1)
    grandmere1.attach_child(pere1)
    pere1.attach_child(enfant1)
    mere1.attach_child(enfant1)
    pere1.attach_child(enfant3)
    mere1.attach_child(enfant3)
    enfant1.attach_child(enfant11)
    enfant11.attach_father(enfant1)
    enfant1.attach_father(pere1)
    enfant1.attach_mother(mere1)
    pere1.attach_father(grandpere1)
    pere1.attach_mother(grandmere1)
    pere2.attach_child(enfant2)
    mere2.attach_child(enfant2)

    # Création de l'arbre généalogique
    trees.add_family_tree(grandpere1)
    trees.add_family_tree(grandmere1)
    trees.add_family_tree(pere1)
    trees.add_family_tree(pere2)
    trees.add_family_tree(mere1)
    trees.add_family_tree(mere2)

    return trees

# Display application main menu and ask user for an option
def choose_main_menu(personne):
    print("\tWelcome to the application << Arbre généalogique >>")
    print("\tyour identity:",personne.firstname,personne.lastname,"Date de naissance(",personne.birthday,")\n\n")

    print('\t\t Ajout ')
    print('\t\t\t1 - Un parent direct') 
    print('\t\t\t2 - Un enfant') 
    print('\t\t Suppression')
    print('\t\t\t3 - Elle-même') 
    print('\t\t\t4 - Un parent direct') 
    print('\t\t\t5 - Un enfant') 
    print('\t\t Consultation')
    print("\t\t\t6 - L’ arbre généalogique global") 
    print("\t\t\t7 - La partie de l’arbre généalogique de sa famille") 
    print("\t\t\t8 - Sa descendance") 
    print("\t\t\t9 - Son ascendance") 
    print("\t\t\t10- Sa descendance et son ascendance")
    print("\t\t\t11- Les personnes ayant un lien de parenté donné") 
    print('\t\t\t12- La liste des personnes sans ascendant')
    print('\t\t\t13- La liste des personnes sans descendant') 
    print('\t\t\t14- La liste des personnes ayant le plus grand nombre d’ascendants vivants')
    print('\n\t\t(0- pour quitter)')

    choice = int(input('Donner le numero de votre choix:'))
    while choice <0 or choice > 14:
        print('Erreur de saisie, donner un choix entre 1 et 14')
        choice = int(input('Donner le numero de votre choix:'))

    return choice

def process_choice():
    return 0

####################### main program #######################

# load Genealogical Tree
trees = load_trees()

# Ask user for identification (or registering as new), or exiting if unknown user
current_user = identify_persone(trees)
if not current_user:
    print("Vous n'etes pas inscrit dans l'arbre, veulleiz quitter ...")
    exit(0)

# call main menu function and read user option
choice = choose_main_menu(current_user)

# call appropriate option function based on user choice
# then display the menu again
while choice!=0:
    if choice==1:
        add_direct_parent(trees,current_user)
    elif choice==2:
        add_person_child(trees,current_user)
    elif choice==3:
        delete_current_user(trees,current_user)       
    elif choice==4:
        delete_direct_parent(trees,current_user)
    elif choice==5:
        delete_children(trees,current_user)
    elif choice==6:
        trees.display()
    elif choice==7:
        current_user.display_tree()
    elif choice==8:
        current_user.display_children()
    elif choice==9:
        current_user.display_parents()
    elif choice==10:
        current_user.display_children()
        current_user.display_parents()
    elif choice==11:
        filter_by_attachment(trees)
    elif choice==12:
        filter_no_attachment(trees,'noparent')
    elif choice==13:
        filter_no_attachment(trees,'nochildren')
    elif choice==14:
        print("Personce avec la plus longue liste d'ascendant:")
        print(trees.persons_longest_parent_path())
    choice = choose_main_menu(current_user)

print('\n\t\tAu revoir....')