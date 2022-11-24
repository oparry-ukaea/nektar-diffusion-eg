///////////////////////////////////////////////////////////////////////////////
//
// File: CWIPIBCsSender.cpp
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
// Description: Sender class for CWIPI-coupled boundary conditions
//
///////////////////////////////////////////////////////////////////////////////

#include <boost/core/ignore_unused.hpp>

#include "CWIPIBCsSender.h"

#include <math.h> ////

using namespace std;

namespace Nektar
{

std::string CWIPIBCsSender::className = GetCFSBndCondFactory().
    RegisterCreatorFunction("CWIPIBCsSender",
                            CWIPIBCsSender::create,
                            "Sender class for CWIPI-coupled boundary conditions.");

CWIPIBCsSender::CWIPIBCsSender(
           const LibUtilities::SessionReaderSharedPtr& pSession,
           const Array<OneD, MultiRegions::ExpListSharedPtr>& pFields,
           const Array<OneD, Array<OneD, NekDouble> >& pTraceNormals,
           const int pSpaceDim,
           const int bcRegion,
           const int cnt)
    : CWIPIBCs(pSession, pFields, pTraceNormals, pSpaceDim, bcRegion, cnt, 1)
{
}

void CWIPIBCsSender::v_Apply(
        Array<OneD, Array<OneD, NekDouble> >               &Fwd,
        Array<OneD, Array<OneD, NekDouble> >               &physarray,
        const NekDouble                                    &time)
{
    int nFields = m_fields.size();

    // // For now, set a single value along the (local) boundary; magnitude = simulation time    
    // for(auto ifld = 0; ifld < nFields; ++ifld)
    // {
    //     MultiRegions::ExpListSharedPtr locExpList = m_fields[ifld]->GetBndCondExpansions()[m_bcRegion];
    //     Array<OneD, NekDouble> BCVals(locExpList->GetNpoints(), time);
    //     locExpList->UpdatePhys() = BCVals;
    //     locExpList->FwdTransBndConstrained(locExpList->GetPhys(), locExpList->UpdateCoeffs());
    // }

    int step = GetStep(time);
    if (IsCouplingStep(step)) {
        // // If this is a coupling step, extract local boundary values
        // Array<OneD, Array<OneD, NekDouble> > SendData(nFields);
        // for(auto ifld = 0; ifld < nFields; ++ifld) {
        //     MultiRegions::ExpListSharedPtr locExpList = m_fields[ifld]->GetBndCondExpansions()[m_bcRegion];
        //     SendData[ifld] = locExpList->GetPhys();
        // }

        //=====================================================================
        // Set dummy send values for debugging
        Array<OneD, Array<OneD, NekDouble> > SendData(nFields);
        for(auto ifld = 0; ifld < nFields; ++ifld) {
            int npoints = m_fields[0]->GetNpoints();
            SendData[ifld] = Array<OneD, NekDouble>(m_fields[ifld]->GetNpoints(), -1);
            Array<OneD, NekDouble> x(npoints), y(npoints);
            m_fields[0]->GetCoords(x, y);
            for (auto ipt=0;ipt<npoints;ipt++)
            {
                SendData[ifld][ipt] = sin(y[ipt]*2*M_PI);
            }
        }
        //=====================================================================

        // Send values
        m_coupling->Send(step, time, SendData, m_couplingVarNames);
    }
}

}
