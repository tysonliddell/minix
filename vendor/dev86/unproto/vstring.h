/* @(#) vstring.h 1.2 92/01/15 21:53:19 */

struct vstring {
    char   *str;			/* string value */
    char   *last;			/* last position */
};

extern struct vstring *vs_alloc(int len);	/* initial allocation */
extern char *vs_realloc(register struct vstring *vp, char *cp);		/* string extension */
extern char *vs_strcpy(register struct vstring *vp, register char *dst, register char *src);		/* copy string */

/* macro to add one character to auto-resized string */

#define	VS_ADDCH(vs,wp,c) \
    ((wp < (vs)->last || (wp = vs_realloc(vs,wp))) ? (*wp++ = c) : 0)
