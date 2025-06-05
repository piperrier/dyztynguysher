
attach rotation_bound.sage
attach kleinjung.sage
#attach kleinjung-list-of-lattices.sage
attach higher_order_roots.sage

Z=Integers()
ZP.<x>=PolynomialRing(Z)
n=110547499294735934596573920716806495615146307355718579549435266277149267619863094991687986227655049181879310236052609641971560327957264468408615218306269241
ad=1008593880; p=1628876881135933; m=161423410553519491417914681351; E=44.88
f,g=lemme_21(n,5,ad,p,m)
g1=g(x+22977)
f1=f(x+22977)-(3*x+18223)*g1

#print f1
#print g1

# Now alpha(f1,2000) is -0.18.
# Within rotation by (jx+k), |j|<=4, |k|<=2^16, the best alpha is reached
# for:
# sage: alpha(f1+(x-26071)*g1,2000)
# -4.6975881658522551
#
# the C version catches this in 82 seconds on nougatine, and 51s on achille
# try: kleinjung -p0max 14 -pb 522 -v -l 7 -M 2e22 -incr 1008593880 110...351

# use f1,g1 above as a base.
f=f1
g=g1


ZP2=PolynomialRing(Z,['X','Y'])
X,Y=ZP2.gens()

def hom(f):
    return ZP2(f(X/Y)*Y^(f.degree()))

ZP3.<t,u,v>=PolynomialRing(Integers(),3)
h=f(t)+(u*t+v)*g(t)


def get_reference(sbound,p):
    complete=matrix(RR,sbound)
    a = flog(p)/(p-1)
    x=ZP.gen()
    t0=cputime()
    for k in range(sbound):
        for l in range(sbound):
            a=flog(p)/(p-1)
            r=f+(k*x+l)*g
            s=alpha_p_simplistic(r,p)-a
            if (valuation(r[r.degree()],p)>=1):
                s -= -p/(p+1)*a
            c=alpha_p_affine_nodisc(r,p)-a
            complete[k,l]=c
        sys.stdout.write(".")
        sys.stdout.flush()
    return complete



def testp(rdict,p,reference):
    rotation_clear(rdict)
    rotation_handle_p(rdict,p)
    allcoeffs=reduce((lambda x,y: x+y),[list(x) for x in
         list(matrix(sbound,sbound,rdict['sarr'])-reference)],[])
    mi,ma=min(allcoeffs), max(allcoeffs);
    res=max(ma,-mi)
    print "Maximal inaccuracy: %e (large means bug!)" % res
    return res < 0.1

def manyp(rdict,plim):
    rotation_clear(rdict)
    t0=cputime()
    for p in prime_range(plim):
        t1=cputime()
        hits=rotation_handle_p(rdict,p)
        print "%r: %.2f seconds, %r hits" % (p,cputime()-t1,hits)
    print "total: %.2f seconds" % (cputime()-t0)



####################################
# To try:

# First task is to fix a size for the sieving area.  We look into
# polynomials h(x,u,v) for
# u integer within the interval [0,sboundu-1]
# v integer within the interval [0,sboundv-1]

# Our purpose here is to see if we can recover f1+(x-26071)*g1. Thus we're
# offsetting by -28000*g

sboundu=10
sboundv=4000
f2=f-28000*g
g2=g


rdict=rotation_init(f2,g2,0,sboundu,0,sboundv)
pmin=3
pmax=100
rotation_clear(rdict)
tt0=cputime()
for p in prime_range(pmin,pmax):
    tt=cputime()
    hits,best,u,v=rotation_handle_p(rdict,p)
    check=alpha(f2+(u*x+v)*g2,p)-alpha(f2+(u*x+v)*g2,pmin-1)
    z=log(10^-20+abs(check-best))
    gooddigits=floor(-z/log(10))
    print "Done %d [%.2f, tot %.2f]." \
            " Best alpha=%.4f, for %d,%d (%d dd ok)" % \
            (p, cputime()-tt, cputime()-tt0, best,u,v,gooddigits)



# Another way to test, relevant only for small arrays because it's
# awfully slow in sage. do an exhaustive test of the reported values, for
# selected p's.

# This first code snippet creates a 2-dimensional array refp with all the
# contributions which _should_ be computed by the rotation program.
#t0=cputime()
#print "First computing reference scores with the naive method"
#refp = get_reference(sbound, p)
#print "Took %.2f seconds" % (cputime()-t0)

# This part calls the root sieve function, and compares
#print "Now with root sieve"
#t0=cputime()
#testp(rdict,p,refp)
#print "Took %.2f seconds" % (cputime()-t0)


# It is also possible to do more extensive testing, by checking what we
# obtain after considering several primes.
# print "First computing # reference scores with the naive method"
# t0=cputime()
# ref2=get_reference(sbound,2)
# ref3=get_reference(sbound,3)
# ref5=get_reference(sbound,5)
# ref7=get_reference(sbound,7)
# print "Took %.2f seconds (total)" % (cputime()-t0)
# 
# print "Now with root sieve"
# t0=cputime()
# rdict=rotation_init(f,g,0,sbound,0,sbound)
# testp(rdict,2,ref2)
# testp(rdict,3,ref3)
# testp(rdict,5,ref5)
# print "Took %.2f seconds (total)" % (cputime()-t0)


# Yet another possible bench
# manyp(rdict,50)


# This is a display function for debugging, but I don't really recall how
# it works.

def zview(m,i0,j0,d):
    ncols = ((m.ncols() - j0) / d).ceil()
    nrows = ((m.nrows() - i0) / d).ceil()
    n=matrix(nrows,ncols)
    for i in range(0,nrows):
        for j in range(0,ncols):
            n[i,j]=m[i0+i*d,j0+j*d]
    return n


# zview(mround(matrix(sbound,sbound,sarr)-complete),1,0,p)
# zview(mround(matrix(sbound,sbound,sarr)-complete),2,1,p)


