import math 
def get_final_v(F, m0, m_dot, t_b): return (F*math.log(m0))/m_dot-(F*math.log(m0-m_dot*t_b))/m_dot
  
def get_final_d(F, m0, m_dot, t_b): return -((F*m_dot*t_b-F*m0)*math.log(m0-m_dot*t_b)-F*m_dot*t_b+F*m0*math.log(m0))/m_dot**2
  
