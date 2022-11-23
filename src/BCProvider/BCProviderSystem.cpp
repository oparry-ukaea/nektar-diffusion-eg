///////////////////////////////////////////////////////////////////////////////
//
// File BCProviderSystem.cpp
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

#include "BCProviderSystem.h"
#include <LibUtilities/BasicUtils/Vmath.hpp>
#include <LibUtilities/TimeIntegration/TimeIntegrationScheme.h>
#include <iostream>
#include <iomanip>
#include <tinyxml.h>

#include <boost/core/ignore_unused.hpp>

using namespace std;

namespace Nektar
{

string BCProviderSystem::className = GetEquationSystemFactory().
    RegisterCreatorFunction("BCProviderSys", BCProviderSystem::create);

BCProviderSystem::BCProviderSystem(
    const LibUtilities::SessionReaderSharedPtr& pSession,
    const SpatialDomains::MeshGraphSharedPtr& pGraph)
    : UnsteadySystem(pSession, pGraph)
{
}

/**
 * @brief Initialisation object for the unsteady diffusion problem.
 */
void BCProviderSystem::v_InitObject(bool DeclareField)
{
    UnsteadySystem::v_InitObject();

    int npoints = m_fields[0]->GetNpoints();

    Array<OneD, NekDouble> xc(npoints), yc(npoints);
    m_fields[0]->GetCoords(xc, yc);

    // ASSERTL0(m_projectionType == MultiRegions::eGalerkin,
    //          "Only continuous Galerkin discretisation supported.");

    // m_nanSteps = 0;

    // Initialise user-defined BCs
    int cnt = 0;
    int Nconditions=m_fields[0]->GetBndConditions().size();
    for (int n = 0; n < Nconditions; ++n)
    {
        std::string userFuncName = m_fields[0]->GetBndConditions()[n]->GetUserDefined();
        auto type = m_fields[0]->GetBndConditions()[n]->GetBoundaryConditionType();
        if (type != SpatialDomains::ePeriodic)
        {
            if (!userFuncName.empty() && userFuncName!="TimeDependent")
            {
                CFSBndCondSharedPtr userDefinedBC = GetCFSBndCondFactory().CreateInstance(
                                        userFuncName,
                                        m_session,
                                        m_fields,
                                        m_traceNormals,
                                        m_spacedim,
                                        n,
                                        cnt);
                m_userDefinedBCs.push_back(userDefinedBC);
            }
            cnt += m_fields[0]->GetBndCondExpansions()[n]->GetExpSize();
        }
    }

    m_ode.DefineImplicitSolve(&BCProviderSystem::DoImplicitSolve, this);
}

/**
 * @brief Unsteady diffusion problem destructor.
 */
BCProviderSystem::~BCProviderSystem()
{
}

void BCProviderSystem::v_GenerateSummary(SummaryList& s)
{
    UnsteadySystem::v_GenerateSummary(s);
}


void BCProviderSystem::DoImplicitSolve(
    const Array<OneD, const Array<OneD, NekDouble> > &inarray,
          Array<OneD,       Array<OneD, NekDouble> > &outarray,
    const NekDouble time,
    const NekDouble lambda)
{
    int nvariables = inarray.size();
    int npoints    = m_fields[0]->GetNpoints();

    // Impose custom BCs (based on user-defined classes)
    for (int i = 0; i < nvariables; ++i)
    {
        Vmath::Vcopy(npoints, inarray[i], 1, outarray[i], 1);
        SetUserDefinedBoundaryConditions(outarray, time);
    }
}

void BCProviderSystem::SetUserDefinedBoundaryConditions(
    Array<OneD, Array<OneD, NekDouble>> &physarray,
    NekDouble                           time)
    {
        int nTracePts  = GetTraceTotPoints();
        int nvariables = physarray.size();

        Array<OneD, Array<OneD, NekDouble>> Fwd(nvariables);
        for (int i = 0; i < nvariables; ++i)
        {
            Fwd[i] = Array<OneD, NekDouble>(nTracePts);
            m_fields[i]->ExtractTracePhys(physarray[i], Fwd[i]);
        }

        if (m_userDefinedBCs.size())
        {
            // Loop over user-defined boundary conditions
            for (auto &x : m_userDefinedBCs)
            {
                x->Apply(Fwd, physarray, time);
            }
        }
    }

} // namespace Nektar
