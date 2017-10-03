from pylayers.util.geomutil import *
from pylayers.util.plotutil import *
import shapely.geometry as shg
import numpy as np
import scipy as sp
from numpy.testing import ( TestCase, assert_almost_equal, assert_raises, assert_equal, assert_, run_module_suite)

class Tesgeu(TestCase):
    def test_onb(self):
        print "testing geomutil.onb"
        A = np.array([[0,0,0,0],[1,2,3,4],[0,0,0,0]])
        B = np.array([[0,0,0,0],[1,2,3,4],[10,10,10,10]])
        v = np.array([[1,1,1,1],[0,0,0,0],[0,0,0,0]])
        T = onb(A,B,v)
        print np.shape(T)
        print T[:,0,:]
        print T[:,1,:]
        print T[:,2,:]
        assert_equal(np.shape(T),(4,3,3))


    def test_ptconvex2(self):
        print "testing geomutil.ptconvex2"

        points  = shg.MultiPoint([(0, 0), (0, 1), (3.2, 1), (3.2, 0.7), (0.4, 0.7), (0.4, 0)])
        polyg   = Polygon(points)
        cvex,ccave   = polyg.ptconvex2() 
        assert_equal(cvex,[-5] )
        assert_equal(ccave,[-1, -2, -3, -4, -6] )
        points  = shg.MultiPoint([(0, 0), (0, 1), (-3.2, 1), (-3.2, 0.7), (-0.4, 0.7), (-0.4, 0)])
        polyg   = Polygon(points)
        cvex,ccave   = polyg.ptconvex2() 
        assert_equal(cvex,[-5] )
        assert_equal(ccave,[-1, -2, -3, -4, -6] )

    def test_is_aligned(self):
        print "testing is_aligned"
        p1 = np.array([0,0])
        p2 = np.array([1,0])
        p3 = np.array([3,0])
        p4 = np.array([4,0])
        p5 = np.array([3,0.1])
        p6 = np.array([4,0.1])
        p7 = np.array([4,0.001])

        b1 = is_aligned4(p1,p2,p3,p4,tol=1e-7)
        b2 = is_aligned4(p1,p2,p5,p6,tol=1e-7)
        b3 = is_aligned4(p1,p2,p3,p7,tol=1e-1)
        b4 = is_aligned4(p1,p2,p3,p7,tol=1e-4)
        assert b1
        assert not b2
        assert b3
        assert not b4

    def test_MATP(self):
        print "test_MATP"
        vl = np.array([0,0,1])  # beam in z direction 
        pl = np.array([1,0,0])  # polar along x

        phi = np.pi/2  # beam in y direction 
        tilt = 0       # no tilt

        M = MATP(vl,pl,phi,tilt,'V')
        vg = np.dot(M,vl)
        pg = np.dot(M,pl)
        np.testing.assert_almost_equal(vg,[0,1,0])  # pointing in y 
        np.testing.assert_almost_equal(pg,[0,0,1])  # polar along z
        M = MATP(vl,pl,phi,tilt,'H')
        vg = np.dot(M,vl)
        pg = np.dot(M,pl)
        np.testing.assert_almost_equal(vg,[0,1,0])  # pointing in y 
        np.testing.assert_almost_equal(pg,[-1,0,0])  # polar along x

    def test_Bthph(self):
        th = np.array([np.pi/2.])
        ph = np.array([np.pi/4.])
        M=np.array([[0,-1,0],[1,0,0],[0,0,1]]) # rotation -np.pi/2 along z
        thg,phg = geu.Bthph(th,ph,M)
        np.testing.assert_almost_equal(thg,np.pi/2.)
        np.testing.assert_almost_equal(phg,-np.pi/4.)



        th = np.array([np.pi/2.])

        ph = np.array([np.pi/4.])

        M=np.array([[1,0,0],[0,0,-1],[0,1,0]])# rotation -np.pi/2 along x
        thg,phg = geu.Bthph(th,ph,M)
        np.testing.assert_almost_equal(thg,3*np.pi/4.)
        np.testing.assert_almost_equal(phg,0.)


        th = np.array([np.pi/2.])
        ph = np.array([np.pi/4.])

        M=np.array([[1,0,0],[0,0,1],[0,-1,0]])# rotation np.pi/2 along x
        thg,phg = geu.Bthph(th,ph,M)

        np.testing.assert_almost_equal(thg,np.pi/4.)
        np.testing.assert_almost_equal(phg,0.)



        th = np.array([np.pi/4])
        ph = np.array([0.])

        M=np.array([[1,0,0],[0,0,1],[0,-1,0]]) # rotation np.pi/2 along x
        thg,phg = geu.Bthph(th,ph,M)
        np.testing.assert_almost_equal(thg,np.pi/2.)
        np.testing.assert_almost_equal(phg,-np.pi/4.)




        M=np.array([[1,0,0],[0,0,-1],[0,1,0]]) # rotation -np.pi/2 along x
        thg,phg = geu.Bthph(th,ph,M)
        np.testing.assert_almost_equal(thg,np.pi/2.)
        np.testing.assert_almost_equal(phg,np.pi/4.)


        M=np.eye(3) 
        thg,phg = geu.Bthph(th,ph,M)


        np.testing.assert_almost_equal(thg,th)
        np.testing.assert_almost_equal(phg,ph)


    def test_intersect3(self):
        print "test_intersect3"
        a = np.array([[1,0,1]]).T
        b = np.array([[10,0,1]]).T
        pg = np.array([[5,0,0]]).T
        u1 = np.array([[0,1,0]]).T
        u2 = np.array([[0,0,1]]).T
        l1 = np.array([3])
        l2 = np.array([3])
        bo,pinter = intersect3(a,b,pg,u1,u2,l1,l2)
        assert bo 

if __name__ == "__main__":
    run_module_suite()
