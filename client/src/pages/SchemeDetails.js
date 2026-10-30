import React from 'react';
import { useParams } from 'react-router-dom';

const SchemeDetails = () => {
  const { id } = useParams();

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        {/* Hero */}
        <div className="bg-gradient-to-r from-cyan-500 to-blue-500 p-8 text-white">
          <h1 className="text-4xl font-bold mb-4">Scheme Details</h1>
          <p className="text-lg opacity-90">Scheme ID: {id}</p>
        </div>

        {/* Content */}
        <div className="p-8 space-y-8">
          <div>
            <h2 className="text-2xl font-bold mb-4">About This Scheme</h2>
            <p className="text-gray-600 mb-4">
              This scheme is designed to provide financial assistance and support to eligible citizens.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4">Eligibility Criteria</h3>
              <ul className="space-y-2 text-gray-700">
                <li>• Age requirement: 18-60 years</li>
                <li>• Income limit: Rs. 5 Lakh per annum</li>
                <li>• Must be Indian citizen</li>
                <li>• Valid documents required</li>
              </ul>
            </div>

            <div>
              <h3 className="text-xl font-bold mb-4">Required Documents</h3>
              <ul className="space-y-2 text-gray-700">
                <li>• Aadhar Card</li>
                <li>• Income Certificate</li>
                <li>• Bank Passbook</li>
                <li>• Identity Proof</li>
              </ul>
            </div>
          </div>

          <div>
            <h3 className="text-xl font-bold mb-4">Benefits</h3>
            <div className="bg-cyan-50 p-6 rounded-lg">
              <p className="text-gray-700">
                Direct financial assistance of up to Rs. 50,000 with flexible repayment terms and minimal interest rates.
              </p>
            </div>
          </div>

          <div className="flex space-x-4">
            <button className="px-8 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-lg font-bold hover:shadow-lg">
              Apply Now
            </button>
            <button className="px-8 py-3 border-2 border-cyan-500 text-cyan-500 rounded-lg font-bold hover:bg-cyan-50">
              Learn More
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SchemeDetails;
