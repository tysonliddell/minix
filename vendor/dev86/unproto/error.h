/* @(#) error.h 1.2 92/01/15 21:53:14 */

extern int errcount;			/* error counter */
extern void error(char *text);			/* default context */
extern void error_where(char *path, int line, char *text);		/* user-specified context */
extern void fatal(char *text);			/* fatal error */
