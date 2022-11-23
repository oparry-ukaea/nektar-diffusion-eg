///////////////////////////////////////////////////////////////////////////////
//
// File BCProviderSystem.h
//
// For more information, please see: http://www.nektar.info
//
// The MIT License
//
// Copyright (c) 2006 Division of Applied Mathematics, Brown University (USA),
// Department of Aeronautics, Imperial College London (UK), and Scientific
// Computing and Imaging Institute, University of Utah (USA).
//
// Permission is hereby granted, free of charge, to any person obtaining a
// copy of this software and associated documentation files (the "Software"),
// to deal in the Software without restriction, including without limitation
// the rights to use, copy, modify, merge, publish, distribute, sublicense,
// and/or sell copies of the Software, and to permit persons to whom the
// Software is furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included
// in all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
// OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
// THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
// DEALINGS IN THE SOFTWARE.
//
// Description: Equation system for the BCProvider solver
//
///////////////////////////////////////////////////////////////////////////////

#ifndef NEKTAR_SOLVERS_ADRSOLVER_EQUATIONSYSTEMS_BCPROVIDER_H
#define NEKTAR_SOLVERS_ADRSOLVER_EQUATIONSYSTEMS_BCPROVIDER_H

#include <SolverUtils/UnsteadySystem.h>
#include <SolverUtils/Diffusion/Diffusion.h>

#include "../BoundaryConditions/CFSBndCond.h"

using namespace Nektar::SolverUtils;

namespace Nektar
{
class BCProviderSystem : public UnsteadySystem
{
public:
    friend class MemoryManager<BCProviderSystem>;

    /// Creates an instance of this class
    static EquationSystemSharedPtr create(
        const LibUtilities::SessionReaderSharedPtr& pSession,
        const SpatialDomains::MeshGraphSharedPtr& pGraph)
    {
        EquationSystemSharedPtr p = MemoryManager<BCProviderSystem>
            ::AllocateSharedPtr(pSession, pGraph);
        p->InitObject();
        return p;
    }
    /// Name of class
    static std::string className;

    /// Destructor
    virtual ~BCProviderSystem() override;

protected:
    virtual void v_GenerateSummary(SummaryList &s) override;

    BCProviderSystem(
        const LibUtilities::SessionReaderSharedPtr& pSession,
        const SpatialDomains::MeshGraphSharedPtr& pGraph);

    virtual void v_InitObject(bool DeclareField = true) override;

    void DoImplicitSolve(
        const Array<OneD, const Array<OneD, NekDouble> >&inarray,
              Array<OneD,       Array<OneD, NekDouble> >&outarray,
        NekDouble time,
        NekDouble lambda);

private:
    std::vector<CFSBndCondSharedPtr> m_userDefinedBCs;
    void SetUserDefinedBoundaryConditions(Array<OneD, Array<OneD, NekDouble>> &physarray, NekDouble time);
};

}

#endif
