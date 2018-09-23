/* This file is part of PyMesh. Copyright (c) 2018 by Qingnan Zhou */
#pragma once

#include <vector>

#include <Core/EigenTypedef.h>
#include <Math/MatrixUtils.h>
#include "EdgeUtils.h"

namespace PyMesh {
namespace ManifoldCheck {

VectorI is_vertex_manifold(const MatrixIr& faces);
MatrixIr is_edge_manifold(const MatrixIr& faces);

}
}
