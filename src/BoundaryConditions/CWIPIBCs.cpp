///////////////////////////////////////////////////////////////////////////////
//
// File: CWIPIBCs.cpp
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
// Description:  Abstract base class for CWIPI-coupled boundary conditions
//
///////////////////////////////////////////////////////////////////////////////

#include <boost/core/ignore_unused.hpp>

#include "CWIPIBCs.h"

#include <cmath>
#include <unistd.h>

using namespace std;

namespace Nektar
{
CWIPIBCs::CWIPIBCs(
           const LibUtilities::SessionReaderSharedPtr& pSession,
           const Array<OneD, MultiRegions::ExpListSharedPtr>& pFields,
           const Array<OneD, Array<OneD, NekDouble> >& pTraceNormals,
           const int pSpaceDim,
           const int bcRegion,
           const int cnt,
           const int initDelay_ms)
    : CFSBndCond(pSession, pFields, pTraceNormals, pSpaceDim, bcRegion, cnt)
{
    sleep(initDelay_ms);
    InitCWIPI(pSession);
    // Set coupling step params - defaults are 0 to 1e9 with a frequency of 1
    pSession->LoadParameter("FirstCouplingStep",m_FirstCouplingStep,0);
    pSession->LoadParameter("CouplingStepFreq",m_CouplingStepFreq,1);
    pSession->LoadParameter("LastCouplingStep",m_LastCouplingStep,1e9);

    // Ensures IsCouplingStep() first returns true when m_FirstCouplingStep is reached
    m_PrevCouplingStep  = m_FirstCouplingStep-m_CouplingStepFreq;
}

void CWIPIBCs::InitCWIPI(const LibUtilities::SessionReaderSharedPtr& pSession){
    std::string errMsg="Unknown err";
    if (pSession->DefinesElement("Nektar/Coupling"))
    {
        TiXmlElement *vCoupling = pSession->GetElement("Nektar/Coupling");
        if (vCoupling->Attribute("TYPE")){
            string vType = vCoupling->Attribute("TYPE");
            if (vType == "Cwipi"){
                m_coupling = SolverUtils::GetCouplingFactory().CreateInstance(vType, m_fields[0]);

                // ToDo: Read and verify coupling variable names
                // Hard-code for now
                m_couplingVarNames = {"BCsVals"};
            } else {
                errMsg="non CWIPI 'type' attribute specified";
            }
        } else {
            errMsg="No 'type' attribute";
        }
    }
    if (! m_coupling){
        NEKERROR(ErrorUtil::efatal, "CWIPIBCs: Error ["+errMsg+"] when reading coupling configuration defined in "+pSession->GetSessionName());
    }
}

int CWIPIBCs::GetStep(const double &time) {
    NekDouble dt;
    m_session->LoadParameter("TimeStep",dt);
    return std::floor(time/dt);
}

bool CWIPIBCs::IsCouplingStep(int step)
{
    if (step >= m_PrevCouplingStep+m_CouplingStepFreq && step <= m_LastCouplingStep){
        m_PrevCouplingStep = step;
        return true;
    } else {
        return false;
    }
}

}
