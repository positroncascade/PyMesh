#!/usr/bin/env python

from distutils.command.build import build
from distutils.command.build_ext import build_ext
import multiprocessing
import os
import os.path
from setuptools import setup, Distribution, Extension
from subprocess import check_call
import shutil
import platform

root_dir = os.path.abspath(os.path.dirname(__file__));
package_dir = os.path.join(root_dir, "python/pymesh");
exec(open(os.path.join(package_dir, 'version.py')).read())

num_cores = multiprocessing.cpu_count();
num_cores = max(1, num_cores);
num_cores = min(num_cores, int(os.environ.get("NUM_CORES", num_cores)));

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False;

    def has_ext_modules(self):
        return True;

class cmake_build(build_ext):
    """
    Python packaging system is messed up.  This class redirect python to use
    cmake for configuration and compilation of pymesh.
    """

    def cleanup(self):
        install_dir = os.path.join(root_dir, "python/pymesh/third_party/lib");
        if os.path.exists(install_dir) and os.path.isdir(install_dir):
            shutil.rmtree(os.path.join(install_dir));

        lib_dir = os.path.join(root_dir, "python/pymesh/lib");
        if os.path.exists(lib_dir) and os.path.isdir(lib_dir):
            shutil.rmtree(os.path.join(lib_dir));

    def build_third_party(self):
        """
        Config and build third party dependencies.
        """
        build_dir = os.path.join(root_dir, "third_party/build");
        if not os.path.isdir(build_dir):
            os.makedirs(build_dir);

        os.chdir(build_dir);
        command = "cmake ..";
        check_call(command.split());
        command = "make -j {}".format(num_cores);
        check_call(command.split());
        command = "make install";
        check_call(command.split());

    def build_pymesh(self):
        """
        Config and build pymesh.
        """
        build_dir = os.path.join(root_dir, "build");
        if not os.path.isdir(build_dir):
            os.makedirs(build_dir);

        os.chdir(build_dir);
        command = "cmake .. -DPythonLibsNew_FIND_VERSION={}".format(
                platform.python_version());
        check_call(command.split());
        command = "make";
        check_call(command.split());
        os.chdir(root_dir);

    def run(self):
        #self.cleanup();
        #self.build_third_party();
        self.build_pymesh();
        #build_ext.run(self);

setup(
        name = "pymesh2",
        description = "Mesh Processing for Python",
        version = __version__,
        author = "Qingnan Zhou",
        author_email = "qnzhou@gmail.com",
        license = "MPL",
        package_dir = {"": "python"},
        packages = ["pymesh", "pymesh.misc", "pymesh.meshutils", "pymesh.wires",
            "pymesh.tests", "pymesh.meshutils.tests", "pymesh.wires.tests"],
        package_data = {"pymesh": [
            "lib/*",
            "third_party/lib/lib*",
            "third_party/lib/*.lib",
            "third_party/lib/*.dll",
            "third_party/lib64/lib*",
            "third_party/lib64/lib*.lib",
            "third_party/lib64/lib*.dll", ]},
        #include_package_data = True,
        cmdclass={
            'build_ext': cmake_build,
            },
        ext_modules=[Extension('foo', ['foo.c'])], # Dummy
        scripts=[
            "scripts/add_element_attribute.py",
            "scripts/add_index.py",
            "scripts/bbox.py",
            "scripts/box_gen.py",
            "scripts/boolean.py",
            "scripts/carve.py",
            "scripts/convex_hull.py",
            "scripts/curvature.py",
            "scripts/distortion.py",
            "scripts/dodecahedron_gen.py",
            "scripts/extract_self_intersecting_faces.py",
            "scripts/fem_check.py",
            "scripts/find_file.py",
            "scripts/fix_mesh.py",
            "scripts/geodesic.py",
            "scripts/highlight_boundary_edges.py",
            "scripts/highlight_degenerated_faces.py",
            "scripts/highlight_non_oriented_edges.py",
            "scripts/highlight_self_intersection.py",
            "scripts/highlight_zero_area_faces.py",
            "scripts/highlight_inverted_tets.py",
            "scripts/hilbert_curve_gen.py",
            "scripts/icosphere_gen.py",
            "scripts/inflate.py",
            "scripts/matrix_gen.py",
            "scripts/mean_curvature_flow.py",
            "scripts/merge.py",
            "scripts/mesh_diff.py",
            "scripts/meshconvert.py",
            "scripts/meshstat.py",
            "scripts/mesh_to_wire.py",
            "scripts/microstructure_gen.py",
            "scripts/minkowski_sum.py",
            "scripts/outer_hull.py",
            "scripts/point_cloud.py",
            "scripts/print_utils.py",
            "scripts/quad_to_tri.py",
            "scripts/remove_degenerated_triangles.py",
            "scripts/remove_duplicated_faces.py",
            "scripts/remove_isolated_vertices.py",
            "scripts/resolve_self_intersection.py",
            "scripts/retriangulate.py",
            "scripts/rigid_transform.py",
            "scripts/scale_mesh.py",
            "scripts/self_union.py",
            "scripts/separate.py",
            "scripts/slice_mesh.py",
            "scripts/subdivide.py",
            "scripts/submesh.py",
            "scripts/tet.py",
            "scripts/tet_boundary.py",
            "scripts/tet_to_hex.py",
            "scripts/triangulate.py",
            "scripts/uv.py",
            "scripts/voxelize.py",
            ],
        url = "https://github.com/qnzhou/PyMesh",
        download_url="https://github.com/qnzhou/PyMesh/tarball/v0.1",
        distclass=BinaryDistribution,
        );
