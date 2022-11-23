///////////////////////////////////////////////////////////////////////////////
//
// File: CWIPIBCsReceiver.cpp
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
// Description: Receiver class for CWIPI-coupled boundary conditions
//
///////////////////////////////////////////////////////////////////////////////

#include <boost/core/ignore_unused.hpp>

#include "CWIPIBCsReceiver.h"

using namespace std;

namespace Nektar
{

std::string CWIPIBCsReceiver::className = GetCFSBndCondFactory().
    RegisterCreatorFunction("CWIPIBCsReceiver",
                            CWIPIBCsReceiver::create,
                            "Receiver class for CWIPI-coupled boundary conditions.");

CWIPIBCsReceiver::CWIPIBCsReceiver(
           const LibUtilities::SessionReaderSharedPtr& pSession,
           const Array<OneD, MultiRegions::ExpListSharedPtr>& pFields,
           const Array<OneD, Array<OneD, NekDouble> >& pTraceNormals,
           const int pSpaceDim,
           const int bcRegion,
           const int cnt)
    : CWIPIBCs(pSession, pFields, pTraceNormals, pSpaceDim, bcRegion, cnt)
{
}

void CWIPIBCsReceiver::v_Apply(
        Array<OneD, Array<OneD, NekDouble> >               &Fwd,
        Array<OneD, Array<OneD, NekDouble> >               &physarray,
        const NekDouble                                    &time)
{
    Array<OneD, Array<OneD, NekDouble> > BCVals(m_couplingVarNames.size());
    int npoints = m_fields[0]->GetNpoints();

    // Set default BC values to 0
    BCVals[0] = Array<OneD, NekDouble>(npoints, 0.0);

    // If this is a coupling step, receive new values
    int step = GetStep(time);
    if (IsCouplingStep(step)) {
        m_coupling->Receive(step, time, BCVals, m_couplingVarNames);
    } 

    // Apply values
    for(auto ii = 0; ii < physarray.size(); ++ii)
    {
        // Get conditions for this field, region
        MultiRegions::ExpListSharedPtr locExpList = m_fields[ii]->GetBndCondExpansions()[m_bcRegion];

        // // Debugging
        // if (m_session->GetComm()->TreatAsRankZero()){
        //     int nprint=5;
        //     std::cout << "time = " << time << "; Receiver setting values: [";
        //     for (auto ii=0;ii<nprint;ii++){
        //         std::cout << BCVals[0][ii] << ", ";
        //     }
        //     std::cout << "]" << std::endl;
        // }

        locExpList->UpdatePhys() = BCVals[ii];

        locExpList->FwdTransBndConstrained(locExpList->GetPhys(), locExpList->UpdateCoeffs());
    }
}

}
