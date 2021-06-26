#!/usr/bin/env python

from illegal_moves import *
from board import *
import copy

class Piece():
    def __init__(self, piece_id, player):
        self.id = piece_id
        self.location = None
        
        self.active = True
        self.player = player

        self.perception = 0
        self.legacy = False
        self.legacy_frequency = False
        self.legacy_duration = False
        
        self.union = []
        self.communication = 0

        self.blindness = 0
        self.oblivion = 0
        self.liberation = 0

    def __eq__(self, piece):
        if self.id == piece.id:
            return True
        else:
            return False

    def __hash__(self):
        return self.id

    def set_location(self, location, board):
        board.check_field(location)
        
        self.location = location
        board.get_field(location).piece = self
        board.get_field(location).check_occupied()
       

    def choose_legacy_effect(self, choice, power):
        assert self.legacy
        assert choice in ['duration', 'frequency']

        duration = {'Time', 'Mind', 'Perception', 'Union', 'Communication',
                    'Oblivion', 'Liberation', 'Blindness', 'Ocean', 'Flame',
                    'Drought', 'Void'}
        frequency - {'Illusion', 'Idea', 'Time', 'Life', 'Death', 'Wave',
                     'Perception', 'Union', 'Impression', 'Communication',
                     'Metamorphosis', 'Oblivion', 'Liberation', 'Blindness',
                     'Earth', 'Ocean', 'Sun', 'Sky', 'Quake', 'Wind', 'Shadow',
                     'Bloodmaker', 'Metalmaker', 'Fog', 'Drought', 'Void',
                     'End', 'Night'}
        

        if choice == 'duration':
            if not power in duration:
                raise IllegalPower('duration')
            self.legacy_duration = True
        elif choice == 'frequency':
            if not power in frequency:
                raise IllegalPower('frequency')
            self.legacy_frequency = True

    def clear_location(self, board):
        board.get_field(self.location).piece = None
        board.get_field(self.location).check_occupied()

        self.location = None

        
    def sleep(self):
        if not self.legacy_frequency:
            self.active = False
            
    def wake(self):
        self.active = True

    def set_perception(self, user):
        if user.legacy_duration:
            self.perception = 4
        else:
            self.perception = 2
    def countdown_perception(self):
        self.perception -= 1
        assert self.perception >= 0

    def activate_union(self, piece):
        self.union.append(piece)
    def deactivate_union(self):
        self.union = []

    def deactivate_legacy(self, choice):
        self.legacy_duration = False
        self.legacy_frequency = False
        self.legacy = False

    def set_communication(self, user):
        if user.legacy_duration:
            self.communication = 2
        else:
            self.communication = 1
    def countdown_communication(self):
        self.communication -= 1
        assert self.communication >= 0

    def activate_illusion(self):
        self.player.illusion.append(self)
        
    def deactivate_illusion(self):
        assert self in self.player.illusion
        self.player.illusion.remove(self)

    def activate_idea(self):
        self.player.idea.append(self)
        
    def deactivate_idea(self):
        assert self in self.idea.player
        self.idea.player.remove(self)

    def set_blindness(self, user):
        if user.legacy_duration:
            self.blindness = 4
        else:
            self.blindness = 2
        
    def countdown_blindness(self):
        self.blindness -= 1
        assert self.blindness >= 0

    def set_oblivion(self, user):
        if user.legacy_duration:
            self.oblivion = 2
        else:
            self.oblivion = 1
    def countdown_oblivion(self):
        self.oblivion -= 1
        assert self.oblivion >= 0

    def set_liberation(self, user):
        if user.legacy_duration:
            self.liberation = 3
        else:
            self.liberation = 2
            
    def countdown_liberation(self):
        self.liberation -= 1
        assert self.liberation >= 0

    def check_immune(self, power):
        if self.perception:
            return True
        
        elif self.type == 'God':
            if power in self.powers:
                return True
            else:
                return False
        elif self.type == 'Heir':
            if power == self.name:
                return True
            else:
                return False

    def check_legal_move_movement(self, target_location, board):
        if not target_location in self.get_movement_options(board):
            raise IllegalMove('range')

    def check_legal_move_general(self, target_location, board):

        if target_location.ocean and self.gender == 'F' and not \
           self.check_immune('Ocean'):
                raise IllegalMove('ocean')

        elif target_location.drought and self.gender == 'M' and not \
             self.check_immune('Drought'):
            raise IllegalMove('drought')

        elif target_location.flame and self.player not in \
             target_location.flame_casters and not self.check_immune("Flame"):
            raise IllegalMove('flame')

        elif target_location.occupied:
            if target_location.piece:
                raise IllegalMove('piece')
            elif target_location.barrier:
                raise IllegalMove('barrier')

        elif target_location.type == "Temple" and \
             target_location.player == self.player:
            raise IllegalMove('temple')

    def move(self, target_location, board):
        board.get_field(self.location).piece = None
        board.get_field(self.location).check_occupied()
        
        self.location = target_location
        board.get_field(target_location).piece = self
        board.get_field(target_location).check_occupied()

    def select_piece(self, piece, power):
        if piece.check_immune(power):
            raise Immune("%s is immune to the power %s." % (piece, power))


class God(Piece):
    def __init__(self, nr, player):
        Piece.__init__(self, nr, player)
        self.type = 'God'

    def get_movement_options(self, board):
        legal_fields = self.location.get_adjacent(board)

        return legal_fields
        
#==============================================================================

class Builder(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'F'
        self.name = "Builder"
        self.powers = ["Earth", "Ocean", "Sky", "Sun"]
        self.symbol = 'e'

class Alchemist(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'F'
        self.name = "Alchemist"
        self.powers = ["Metalmaker", "Bloodmaker", "Fog", "Flame"]
        self.symbol = 'g'

class Connector(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'F'
        self.name = "Connector"
        self.powers = ["Union", "Impression", "Communication", "Familiarity"]
        self.symbol = 'b'
        
class Wiper(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'F'
        self.name = 'Wiper'
        self.powers = ["Death", "Blindness", "Oblivion", "Liberation"]
        self.symbol = 'd'

class Mover(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'M'
        self.name = 'Mover'
        self.powers = ["Quake", "Wave", "Wind", "Shadow"]
        self.symbol = 'f'

class Consumer(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'M'
        self.name = 'Consumer'
        self.powers = ["Void", "Drought", "End", "Night"]
        self.symbol = 'h'

class Gifter(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'M'
        self.name = 'Gifter'
        self.powers = ["Life", "Perception", "Mind", "Legacy"]
        self.symbol = 'a'

class Director(God):
    def __init__(self, nr, player):
        God.__init__(self, nr, player)
        self.gender = 'M'
        self.name = 'Director'
        self.powers = ["Time", "Illusion", "Idea", "Metamorphosis"]
        self.symbol = 'c'

#==============================================================================

class FemaleHeir(Piece):
    def __init__(self, nr, player):
        Piece.__init__(self, nr, player)
        self.gender = 'F'
        self.type = 'Heir'

    def get_movement_options(self, board):
        legal_fields = self.location.get_adjacent_horizontal(board)

        return legal_fields

class MaleHeir(Piece):
    def __init__(self, nr, player):
        Piece.__init__(self, nr, player)
        self.gender = 'M'
        self.type = 'Heir'

    def get_movement_options(self, board):
        legal_fields = self.location.get_adjacent_diagonal(board)

        return legal_fields

#==============================================================================

class Union(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Union"
        self.symbol = 'm'

    def use_power(self, piece_1, piece_2):
        self.select_piece(piece_1, self.name)
        self.select_piece(piece_2, self.name)

        if piece_1.active != piece_2.active:
            raise IllegalPower('union')

        piece_1.activate_union(piece_2)
        piece_2.activate_union(piece_1)
        
        self.sleep()
        

class Impression(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Impression"
        self.symbol = 'n'

    def use_power(self, piece, board):
        self.select_piece(piece, self.name)

        if board.get_field(piece.location).type == \
           "Temple Area":
            raise IllegalPower('impression')

        old_location = copy.copy(self.location)
        piece_location = copy.copy(piece.location)

        board.get_field(old_location).piece = piece
        board.get_field(piece_location).piece = self

        self.location = board.get_field(piece_location)
        piece.location = board.get_field(old_location)

        self.sleep()


class Communication(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Communication"
        self.symbol = 'o'

    def use_power(self, piece):
        self.select_piece(piece, self.name)

        self.activate_communication()

        self.sleep()

class Familiarity(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Familiarity"
        self.symbol = 'p'

    def use_power(self, piece, pieces):
        raise NotImplementedError

class Death(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Death"
        self.symbol = 'u'

    def use_power(self, piece):
        self.select_piece(piece, self.name)

        if not piece.active:
            raise IllegalPower('death')

        piece.sleep()
        self.sleep()

class Blindness(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Blindness"
        self.symbol = 'v'

    def use_power(self, piece):
        self.select_piece(piece, self.name)

        piece.set_blindness(self)
        self.sleep()

class Oblivion(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Oblivion"
        self.symbol = 'w'

    def use_power(self, piece):
        self.select_piece(piece, self.name)

        if not piece.passive:
            raise IllegalPower('oblivion')

        piece.set_oblivion(self)
        self.sleep()

class Liberation(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Liberation"
        self.symbol = 'x'

    def use_power(self, piece):
        self.select_piece(piece, self.name)

        piece.set_liberation(self)
        self.sleep()


class Earth(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Earth"
        self.symbol = 'y'

    def use_power(self, barriers, board, field_1, field_2 = None):
        barriers.place_barrier(field_1, board)
        if field_2:
            barriers.place_barrier(field_2, board)

        self.sleep()

class Ocean(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Ocean"
        self.symbol = 'z'

    def use_power(self, field, board):
        board.check_field(field)
        adjacent_fields = field.get_adjacent(board)
        
        for field in adjacent_fields:
            field.ocean = True
            
        self.sleep()
        

class Sky(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Sky"
        self.symbol = 'A'

    def use_power(self, piece, board):
        self.select_piece(piece, self.name)

        adjacent = self.location.check_adjacent(piece.location, board)

        if not adjacent:
            raise IllegalPower('sky')

        assert not (0 == diff_x == diff_y)

        if self.location.x > piece.location.x:
            new_x = piece.location.x - 1
        elif self.location.x == piece.location.x:
            new_x = self.location.x
        else:
            new_x = piece.location.x + 1

        if self.location.y > piece.location.y:
            new_y = piece.location.y - 1
        elif self.location.y == piece.location.y:
            new_y = self.location.y
        else:
            new_y = piece.location.y + 1

        new_field = PhantomField(new_x, new_y)
        board.check_field(new_field)
        new_field = board.get_field(new_field)
        
        self.check_legal_move_general(new_field, board)
        self.move(new_field, board)

        self.sleep()
        

class Sun(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Sun"
        self.symbol = 'B'

    def use_power(self, field, board):
        legal_locations = self.find_legal_locations(field, board)
        legal_locations = self.filter_legal_locations(legal_locations,
                                                       board)

        if not field in legal_locations:
            raise IllegalPower('sun')

        self.move(field, board)

        self.sleep()

    def find_legal_locations(self, field, board):

        legal_locations = set([])

        for i in range(self.location.x - 2, self.location.x + 3):
            for j in range(self.location.y - 2, self.location.y + 3):

                if self.location.x == i and self.location.y == j:
                    continue
                elif self.location.x != i and self.location.y != j:
                    continue
                else:
                    legal_locations.add(PhantomField(i, j))

        return legal_locations
    

    def filter_legal_locations(self, legal_locations, board):
        filtered_locations = []
        
        direction_1 = []
        direction_2 = []
        direction_3 = []
        direction_4 = []

        for location in legal_locations:
            if self.location.y > location.y:
                direction_1.append(location)
            elif self.location.x > location.x:
                direction_2.append(location)
            elif self.location.y < location.y:
                direction_3.append(location)
            elif self.location.x < location.x:
                direction_4.append(location)

        direction_1.sort(key= lambda field: field.y, reverse=True)
        direction_2.sort(key= lambda field: field.x, reverse=True)
        direction_3.sort(key= lambda field: field.y)
        direction_4.sort(key= lambda field: field.x)

        all_directions = [direction_1, direction_2, direction_3, direction_4]

        for direction in all_directions:
            for field in direction:
                try:
                    board.check_field(field)
                    self.check_legal_move_general(board.get_field(field), board)
                    filtered_locations.append(field)
                except (IllegalMove, IllegalField):
                    break

        return filtered_locations
            

class Metalmaker(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Metalmaker"
        self.symbol = 'G'

    def use_power(self, field, barriers, board):
        
        if barriers.count == 3:
            raise IllegalPower('metalmaker')

        board.check_field(field)
        self.check_legal_move_movement(field, board)
        self.check_legal_move_general(field, board)

        old_field = self.location

        self.move(old_field, board)
        barriers.place_barrier(field, board)

        self.sleep()

class Bloodmaker(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Bloodmaker"
        self.symbol = 'H'

    def use_power(self, piece, barrier_field, barriers, board):
        self.select_piece(piece, self.name)
        
        if not board.get_field(barrier_field).barrier:
            raise IllegalBarrier('no barrier')
        
        if not piece.location.check_adjacent(barrier_field, board):
            raise IllegalPower('bloodmaker')

        board.get_field(barrier_field).occupied = False

        piece_location = copy.copy(piece.location)

        piece.move(barrier_field, board)
        barriers.move_barrier(barrier_field, piece_location)

        self.sleep()

class Fog(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Fog"
        self.symbol = 'I'

    def use_power(self, piece_1, piece_2, board):
        self.select_piece(piece_1, self.name)
        self.select_piece(piece_2, self.name)

        if not piece_1.location.check_adjacent(piece_2.location, board):
            raise IllegalPower('fog')

        piece1_location = copy.copy(piece_1.location)
        piece2_location = copy.copy(piece_2.location)

        board.get_field(piece1_location).piece = piece_2
        board.get_field(piece2_location).piece = piece_1

        piece_1.location = board.get_field(piece2_location)
        piece_2.location = board.get_field(piece1_location)

        self.sleep()

class Flame(FemaleHeir):
    def __init__(self, nr, player):
        FemaleHeir.__init__(self, nr, player)
        self.name = "Flame"
        self.symbol = 'J'

    def use_power(self, board):
        for field in find_flame_locations(board):
            board.get_field(field).activate_flame(self)

        self.sleep()


    def find_flame_locations(self, board):

        flame_locations = set(self.location.get_adjacent(board))

        for i in range(self.location.x - 2, self.location.x + 3):
            for j in range(self.location.y - 2, self.location.y + 3):

                if self.location.x == i and self.location.y == j:
                    continue
                elif self.location.x != i and self.location.y != j:
                    continue
                else:
                    try:
                        board.check_field(PhantomField(i, j))
                        flame_locations.add(PhantomField(i, j))
                    except IllegalField:
                        pass
                    
        return flame_locations
        


#==============================================================================

class Life(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Life"
        self.symbol = 'i'

    def use_power(self, piece):
        self.select_piece(piece, self.name)
        if piece.active:
            raise IllegalPower('life')

        piece.active = True
        self.sleep()

class Perception(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Perception"
        self.symbol = 'j'

    def use_power(self, piece):
        self.select_piece(piece, self.name)

        piece.set_perception(self)
        self.sleep()

class Mind(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Mind"
        self.symbol = 'k'

    def use_power(self, board):
        temple = board.get_field(self.player.temple)
        temple.set_mind(self)

        self.sleep()

class Legacy(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Legacy"
        self.symbol = 'l'

    def use_power(self, piece):
        self.select_piece(piece, self.name)
        if piece.legacy:
            raise IllegalPower('legacy')

        piece.legacy = True
        self.sleep()

class Time(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Time"
        self.symbol = 'q'

    def use_power(self, player):
        
        player.set_time_pieces(self)
        player.set_time_count()
        self.sleep()
        

class Illusion(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Illusion"
        self.symbol = 'r'

    def use_power(self, piece):

        self.select_piece(piece, self.name)

        piece.player.add_piece_illusion(piece)
        self.sleep()
        

class Idea(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Idea"
        self.symbol = 's'

    def use_power(self, piece):
        self.select_piece(piece, self.name)
        piece.player.add_piece_idea(piece)
        self.sleep()
        

class Metamorphosis(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Metamorphosis"
        self.symbol = 't'

    def use_power(self, piece_1, piece_2, board, players):
        if piece_1.player == self.player:
            raise IllegalPower('metamorphosis')

        if piece_2.player == self.player:
            raise IllegalPower('metamorphosis')

        if piece_1.type == 'God':
            raise IllegalPower('god')

        if piece_2.type == 'God':
            raise IllegalPower('god')

        player_1 = copy.copy(piece_1.player)
        player_2 = copy.copy(piece_2.player)

        piece1_location = copy.copy(piece_1.location)
        piece2_location = copy.copy(piece_2.location)

        board.get_field(piece1_location).piece = piece_2
        board.get_field(piece2_location).piece = piece_1

        piece_1.location = board.get_field(piece2_location)
        piece_2.location = board.get_field(piece1_location)

        

class Quake(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, location, player)
        self.name = "Quake"
        self.symbol = 'C'

class Wave(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Wave"
        self.symbol = 'D'

class Wind(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Wind"
        self.symbol = 'E'

class Shadow(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Shadow"
        self.symbol = 'F'

class Void(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Void"
        self.symbol = 'K'

class Drought(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Drought"
        self.symbol = 'L'

class End(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "End"
        self.symbol = 'M'

class Night(MaleHeir):
    def __init__(self, nr, player):
        MaleHeir.__init__(self, nr, player)
        self.name = "Night"
        self.symbol = 'N'