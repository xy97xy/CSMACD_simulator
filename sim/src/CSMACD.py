# CSMA/CD Simulator CS 4450 Project
# Xiaoyu Yan (xy97)
# This is CSMA/CD simulator:
# This module simulates how the CSMA/CD would act in response to 
# multiple mediums contesting a broadcast slot.
from __future__ import print_function

class CSMA_CD_sim():
  """
    Simulator that handles the incoming mMdiums using CSMA/CD 
    These are some of the possible printouts for debugging
    Progress so far:
     A | a0  a0      a0  a1
     B | b0      b0      b0
     C | c0  c0          c0
     D | d0      d0          d0
     E | e0      e0
-------| --  --  --  --  --  --
 Slot #|  0   1   2   3   4   5
    Current state:

    Source | Current frame | Num. Collisions | Possible slots
    -------+---------------+-----------------+----------------------------
    A      | a1            | 1               | 6
    B      | b0            | 3               | 6,7,8,9,10,11,12
    C      | c0            | 3               | 6,7,8,9,10,11,12
    D      | d1            | 0               | 6
    E      | e0            | 2               | 6

  """
  
  def __init__ (self,sources):
    assert isinstance(sources,list)
    self._sources = sources 
    self._slots = []
    self._slot_number = 0
    self._time = 0

  def print_sources(self):
    print ("\nCurrent sources: ")
    for i in self._sources:
      print (" %s " %(i.info()), end='')
    print('')

  def print_progress(self):
    print ("\nProgress so far:")
    print("S# | ", end='')
    for i in range(len(self._sources)):
      print( "" + self._sources[i].info() + "  | ", end="")
    print("")
    for i in self._slots:
      for j in i:
        print(" "+ j + " |", end="")
      print("")    
    print("")    

  def print_curr_state(self):
    print ("\nCurrent State:")
    print ("Src|Curr F|Col.|Poss. Slots")
    print ("---+------+----+-----------")
    #print out current sources
    for i in range(len(self._sources)):
      print( " "+self._sources[i].info() + " | ", end='')
      print( " "+self._sources[i].info()+\
        str(self._sources[i].currFrame()) + "  | ", end = '')
      print( ""+ str(self._sources[i].collisions())\
         + "  | ", end = '')
      print( str(self._sources[i].possibleSlots()))
  
  def print_choices(self):
    print ("\nPossibilities for slot %s" %(self._slot_number))
    for i in self._sources:
      if self._slot_number in i.possibleSlots():
        print(" %s%s "%(i.info(),i.currFrame()),end='')
    print ("")

  def cycle(self, choices):
    """
    choices: array of choices corresponding to each src
    """
    assert isinstance(choices,list)
    sl = []
    sl.append(str(self._slot_number))
    self._slot_number += 1
    if choices.count(1)>1:
      for i in range(len(self._sources)):
        if choices[i]:
          self._sources[i].collision(self._slot_number)
          sl.append(self._sources[i].info()+str(self._sources[i].currFrame()))
        else:
          self._sources[i].cycle()
          sl.append("  ")
    else:
      for i in range(len(self._sources)):
        if choices[i]:
          self._sources[i].success(self._slot_number)
          sl.append(self._sources[i].info()+str(self._sources[i].currFrame()))
        else:
          self._sources[i].cycle()
          sl.append("  ")
    self._slots.append(sl)

    
    
class Source():
  """
  Broadcase medium from a transmission. Shared with other sources and resolved using
  CSMA/CD
  """

  def currFrame(self):
    return self._curr_frame

  def collisions(self):
    return self._collisions
  def info(self):
    return self._name
  def possibleSlots(self):
    return self._possible_slots

  def __init__ (self,name,num_frames):
    assert isinstance(name,str)
    assert isinstance(num_frames,int)
    self._name = name
    self._num_frames = num_frames
    self._collisions = 0
    self._curr_frame = 0
    self._possible_slots = [0] #slot numbers that are possible

  def collision(self, slot_number):
    assert isinstance(slot_number,int)
    self._collisions += 1
    cur_slot = self._possible_slots
    self._possible_slots = [i for i in \
      range(slot_number,slot_number+2**self._collisions)]

  def success(self, slot_number):
    assert isinstance(slot_number,int)
    self._collisions = 0
    self._curr_frame += 1
    self._num_frames -= 1
    self._possible_slots = [slot_number]
    return self._num_frames

  def cycle(self):
    for i in range(len(self._possible_slots)):
      self._possible_slots[i] += 1
