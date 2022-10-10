///////////////////////////////////////////////////////////////////////////////
//
// File: ChaoticBCs.cpp
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
// Description: Chaotic boundary condition
//
///////////////////////////////////////////////////////////////////////////////

#include <boost/core/ignore_unused.hpp>

#include "ChaoticBCs.h"

using namespace std;

namespace Nektar
{

std::string ChaoticBCs::className = GetCFSBndCondFactory().
    RegisterCreatorFunction("ChaoticBCs",
                            ChaoticBCs::create,
                            "Chaotic boundary condition.");

ChaoticBCs::ChaoticBCs(
           const LibUtilities::SessionReaderSharedPtr& pSession,
           const Array<OneD, MultiRegions::ExpListSharedPtr>& pFields,
           const Array<OneD, Array<OneD, NekDouble> >& pTraceNormals,
           const int pSpaceDim,
           const int bcRegion,
           const int cnt)
    : CFSBndCond(pSession, pFields, pTraceNormals, pSpaceDim, bcRegion, cnt)
{
    // For each field
    for(auto ii = 0; ii < pFields.size(); ++ii)
    {
        std::string varName = pSession->GetVariable(ii);
        std::string funcName = GetBCFunctionName(varName);
        auto conditions = pFields[ii]->GetBndConditions();
        auto conditionExpLists = pFields[ii]->GetBndCondExpansions();
        for (auto jj=0;jj<conditions.size();++jj)
        {
            // For each conditions defined for this field
            std::string userFuncType = conditions[jj]->GetUserDefined();
            if (userFuncType==className)
            {
                if (pSession->DefinesFunction(funcName))
                {
                    bool funcAlreadyDefinedForVar = m_funcDefs.find(ii) != m_funcDefs.end();
                    if (funcAlreadyDefinedForVar)
                    {
                        NEKERROR(ErrorUtil::efatal, "Only one" + className + " BC is allowed per field - multiple declarations for field "+varName);
                    }
                    else
                    {
                        SolverUtils::SessionFunctionSharedPtr func = MemoryManager<SolverUtils::SessionFunction>::AllocateSharedPtr(pSession, pFields[ii], funcName, true);
                        m_funcDefs[ii] = MemoryManager<FuncDef>::AllocateSharedPtr(varName,conditionExpLists[jj],0,func);
                    }
                }
                else
                {
                    // Bail out if no associated function is defined by the session
                    NEKERROR(ErrorUtil::efatal, className+" declared for field "+varName+"; session must define a function called "+funcName);
                }
            }
        } 
    }
}

std::string ChaoticBCs::GetBCFunctionName(int varIdx)
{
    return GetBCFunctionName(m_session->GetVariable(varIdx));
}

std::string ChaoticBCs::GetBCFunctionName(std::string varName)
{
    return varName+"BCs";
}

void ChaoticBCs::v_Apply(
        Array<OneD, Array<OneD, NekDouble> >               &Fwd,
        Array<OneD, Array<OneD, NekDouble> >               &physarray,
        const NekDouble                                    &time)
{
    //boost::ignore_unused(Fwd, physarray, time);

    boost::ignore_unused(Fwd);
    for(auto ii = 0; ii < physarray.size(); ++ii)
    {
        auto entry = m_funcDefs.find(ii);
        if (entry != m_funcDefs.end())
        {
            FuncDefShPtr def = entry->second;
            Array<OneD, NekDouble> pArray;
            (def->m_func)->Evaluate(def->m_fieldName, pArray, time, def->m_domain);

            MultiRegions::ExpListSharedPtr locExpList = def->m_field;
            int npoints = locExpList->GetNpoints();
            Array<OneD, NekDouble> x0(npoints, 0.0);
            Array<OneD, NekDouble> x1(npoints, 0.0);
            Array<OneD, NekDouble> x2(npoints, 0.0);

            locExpList->GetCoords(x0, x1, x2);
            NekDouble val = pArray[0];

            locExpList->SetCoeff(0, val);               
            locExpList->SetPhys(0, locExpList->GetCoeff(0));
        }
    }
}

}
