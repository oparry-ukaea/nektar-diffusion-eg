///////////////////////////////////////////////////////////////////////////////
//
// File: CWIPIBCs.h
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
// Description: Abstract base class for CWIPI-coupled boundary conditions
//
///////////////////////////////////////////////////////////////////////////////

#ifndef NEKTAR_SOLVERS_COMPRESSIBLEFLOWSOLVER_BNDCOND_CWIPIBCs
#define NEKTAR_SOLVERS_COMPRESSIBLEFLOWSOLVER_BNDCOND_CWIPIBCs

#include "CFSBndCond.h"
#include <SolverUtils/Core/Coupling.h>
#include <SolverUtils/Core/SessionFunction.h>
#include <FieldUtils/Interpolator.h>


namespace Nektar
{

/**
* @brief Abstract base class for CWIPI-coupled boundary conditions
*/
class CWIPIBCs : public CFSBndCond
{
    public:

    protected:
        CWIPIBCs(const LibUtilities::SessionReaderSharedPtr& pSession,
               const Array<OneD, MultiRegions::ExpListSharedPtr>& pFields,
               const Array<OneD, Array<OneD, NekDouble> >& pTraceNormals,
               const int pSpaceDim,
               const int bcRegion,
               const int cnt);

        virtual ~CWIPIBCs(void){};

        int m_CouplingStepFreq;
        std::vector<std::string> m_couplingVarNames;
        int m_FirstCouplingStep;
        // The final step on which to send/receive coupling data
        int m_LastCouplingStep;
        // The step on which coupling data was last sent/received
        int m_PrevCouplingStep;
        int GetStep(const double &time);
        void InitCWIPI(const LibUtilities::SessionReaderSharedPtr& pSession);
        bool IsCouplingStep(int step);

        // Copy of the pointer to the coupling object for convenience
        SolverUtils::CouplingSharedPtr m_coupling;
    private:
};

}

#endif
