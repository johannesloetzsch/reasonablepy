/* File:      swig_xsb.h
** Author(s): Markus Schatten
** Contact:   markus_dot_schatten_at_foi_dot_hr
** 
** Copyright (C) Faculty of Organization and Informatics, 2006.
** 
** Reasonable Python is free software; you can redistribute it and/or modify 
** it under the terms of the GNU Library General Public License as published 
** by the Free Software Foundation; either version 2 of the License, or (at 
** your option) any later version.
** 
** Flopy is distributed in the hope that it will be useful, but WITHOUT ANY
** WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
** FOR A PARTICULAR PURPOSE.  See the GNU Library General Public License for
** more details.
** 
** You should have received a copy of the GNU Library General Public License
** along with Flopy; if not, write to the Free Software Foundation,
** Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
**
** 
*/

#include <stdio.h>
#include "cinterf.h"
#include "builtin.h"

/*extern int xsb_init(int, char **);
extern int xsb_query_string(char *);
extern int xsb_next();
extern int xsb_next_string(VarString*,char*);
extern int xsb_get_last_answer_string(char*,int,int*);
extern int xsb_close_query();
extern int xsb_close();
extern int xsb_get_last_error_string(char*,int,int*);

extern char *xsb_executable_full_path(char *);
extern char *strip_names_from_path(char*, int);*/

extern char **create_string_array( int );
extern char **assign_string( char **, char *, int );
extern void print_string_array( char ** , int );
extern void release_string_array( char **, int );
extern char *pcharlist2string( unsigned long, int );
extern int *intpointer( int );


extern int  ptoc_int(int);	
						/* defined in builtin.c */
extern double  ptoc_float(int);
						/* defined in builtin.c */
extern char*  ptoc_string(int);
						/* defined in builtin.c */
extern char*  ptoc_longstring(int);
						/* defined in builtin.c */
//extern char*  ptoc_abs(int);

extern void   ctop_int(int, int);
						/* defined in builtin.c */
extern void   ctop_float(int, double);
						/* def in builtin.c */
/*extern void   ctop_string(int, char*);*/
						/* def in builtin.c */
/*extern void   extern_ctop_string(int, char*);*/
						/* def in builtin.c */
/*extern int    ctop_abs(int, char*);*/

/*extern char* string_find(char*, int);*/		/* defined in psc.c	*/

/*extern int   ctop_term(char*, char*, reg_num);
extern int   ptoc_term(char*, char*, reg_num);*/

/*======================================================================*/
/* Low level C interface						*/
/*======================================================================*/


extern unsigned long  reg_term(int);

extern short  c2p_int(int, unsigned long);
extern short  c2p_float(double, unsigned long);
extern short  c2p_string(char *, unsigned long);
extern short  c2p_list(unsigned long);
extern short  c2p_nil(unsigned long);
extern void  ensure_heap_space(int, int);
extern short  c2p_functor(char *, int, unsigned long);
extern void  c2p_setfree(unsigned long);
extern void  c2p_chars(char *str, int regs_to_protect, unsigned long term);


extern int    p2c_int(unsigned long);
extern double    p2c_float(unsigned long);
extern char*     p2c_string(unsigned long);
extern char*     p2c_functor(unsigned long);
extern int       p2c_arity(unsigned long);
extern char*     p2c_chars(unsigned long,char *,int);

extern unsigned long  p2p_arg(unsigned long, int);
extern unsigned long  p2p_car(unsigned long);
extern unsigned long  p2p_cdr(unsigned long);
extern unsigned long  p2p_new();
extern short         p2p_unify(unsigned long, unsigned long);
/*extern short         p2p_call(unsigned long);
extern void	      p2p_funtrail();*/
extern unsigned long  p2p_deref(unsigned long);

extern short  is_var(unsigned long);
extern short  is_int(unsigned long);
extern short  is_float(unsigned long);
extern short  is_string(unsigned long);
extern short  is_atom(unsigned long);
extern short  is_list(unsigned long);
extern short  is_nil(unsigned long);
extern short  is_functor(unsigned long);
extern short  is_charlist(unsigned long,int*);
extern short  is_attv(unsigned long);

extern int   c2p_term(char*, char*, unsigned long);
extern int   p2c_term(char*, char*, unsigned long);

/*======================================================================*/
/* Other utilities							*/
/*======================================================================*/


//extern char *vfile_open(/* vfile, func, func, func, func, func */);
//extern char *vfile_obj(/* vfile */);

/*======================================================================*/
/* Routines to call xsb from C						*/
/*======================================================================*/

extern int  xsb_init(int, char **);
extern int  xsb_init_string(char *);
extern int  xsb_command();
extern int  xsb_command_string(char *);
extern int  xsb_query();
extern int  xsb_query_string(char *);
extern int  xsb_query_string_string(char*,VarString*,char*);
extern int  xsb_query_string_string_b(char*,char*,int,int*,char*);
extern int  xsb_next();
extern int  xsb_next_string(VarString*,char*);
extern int  xsb_next_string_b(char*,int,int*,char*);
extern int  xsb_get_last_answer_string(char*,int,int*);
extern int  xsb_close_query();
extern int  xsb_close();
extern int  xsb_get_last_error_string(char*,int,int*);

extern void  print_pterm(Cell, int, VarString*);
extern char *p_charlist_to_c_string(unsigned long term, VarString *buf,
					char *in_func, char *where);

