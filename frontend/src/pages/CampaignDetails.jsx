import { useState, useEffect } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { Calendar, Users, Target, Clock, ArrowLeft, Share2, Heart } from "lucide-react"
import mockCampaigns from "../lib/campaigns.js"

export default function CampaignDetails() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [campaign, setCampaign] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [donationAmount, setDonationAmount] = useState("")

  useEffect(() => {
    const fetchCampaign = async () => {
      try {
        setLoading(true)
        setError(null)

        /* 
        // Uncomment when backend API is ready
        const response = await fetch(`/api/campaigns/${id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            // 'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        
        if (!response.ok) {
          throw new Error(`Campaign not found`)
        }
        
        const data = await response.json()
        setCampaign(data)
        */

        // Mock data lookup
        const foundCampaign = mockCampaigns.find(c => c.campaign_id === id)
        if (!foundCampaign) {
          throw new Error("Campaign not found")
        }
        setCampaign(foundCampaign)
        setLoading(false)
        
      } catch (err) {
        console.error('Error fetching campaign:', err)
        setError(err.message)
        setLoading(false)
      }
    }

    if (id) {
      fetchCampaign()
    }
  }, [id])

  const handleDonate = () => {
    // Handle donation logic here
    console.log(`Donating $${donationAmount} to campaign ${id}`)
    // You can navigate to payment page or open payment modal
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading campaign...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error || !campaign) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center py-12">
            <div className="text-red-500 mb-4">
              <svg className="h-12 w-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Campaign Not Found</h3>
            <p className="text-gray-600 mb-4">{error}</p>
            <button 
              onClick={() => navigate('/all-campaigns')} 
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Back to Campaigns
            </button>
          </div>
        </div>
      </div>
    )
  }

  const progressPercentage = Math.min((campaign.raised_amount / campaign.goal_amount) * 100, 100)
  
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount)
  }

  const getDaysRemaining = () => {
    const today = new Date()
    const endDate = new Date(campaign.end_date)
    const diffTime = endDate - today
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    return diffDays > 0 ? diffDays : 0
  }

  const getCategoryStyle = (category) => {
    const styles = {
      charity: "bg-blue-500 text-white",
      medical: "bg-red-500 text-white",
      education: "bg-green-500 text-white",
      emergency: "bg-orange-500 text-white",
      personal: "bg-purple-500 text-white"
    }
    return styles[category] || styles.personal
  }

  const daysRemaining = getDaysRemaining()

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Back Button */}
        <button
          onClick={() => navigate('/all-campaigns')}
          className="mb-6 flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to All Campaigns
        </button>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {/* Campaign Image */}
            <div className="relative aspect-video mb-6 rounded-xl overflow-hidden">
              <img
                src={campaign.image}
                alt={campaign.title}
                className="w-full h-full object-cover"
              />
              <div className="absolute top-4 left-4">
                <span className={`inline-flex items-center rounded-full px-3 py-1 text-sm font-semibold capitalize ${getCategoryStyle(campaign.category)}`}>
                  {campaign.category}
                </span>
              </div>
            </div>

            {/* Campaign Title and Description */}
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">{campaign.title}</h1>
              <p className="text-lg text-gray-700 mb-6">{campaign.short_description}</p>
              <div className="prose prose-gray max-w-none">
                <p>{campaign.long_description}</p>
              </div>
            </div>

            {/* Campaign Stats */}
            <div className="bg-white rounded-xl p-6 mb-6">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-blue-600">{formatCurrency(campaign.raised_amount)}</div>
                  <div className="text-sm text-gray-500">Raised</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-gray-900">{formatCurrency(campaign.goal_amount)}</div>
                  <div className="text-sm text-gray-500">Goal</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-green-600">{progressPercentage.toFixed(0)}%</div>
                  <div className="text-sm text-gray-500">Funded</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-orange-600">{daysRemaining}</div>
                  <div className="text-sm text-gray-500">Days Left</div>
                </div>
              </div>
            </div>

            {/* Campaign Meta */}
            <div className="bg-white rounded-xl p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Campaign Details</h3>
              <div className="space-y-3">
                <div className="flex items-center gap-3 text-gray-600">
                  <Calendar className="h-5 w-5" />
                  <span>Started on {new Date(campaign.start_date).toLocaleDateString()}</span>
                </div>
                <div className="flex items-center gap-3 text-gray-600">
                  <Clock className="h-5 w-5" />
                  <span>Ends on {new Date(campaign.end_date).toLocaleDateString()}</span>
                </div>
                <div className="flex items-center gap-3 text-gray-600">
                  <Users className="h-5 w-5" />
                  <span>Created by {campaign.creator_id}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Donation Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-8">
              <div className="bg-white rounded-xl p-6 shadow-lg">
                {/* Progress Bar */}
                <div className="mb-6">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700">Progress</span>
                    <span className="text-sm font-medium text-blue-600">{progressPercentage.toFixed(0)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className="bg-blue-600 h-3 rounded-full transition-all duration-300"
                      style={{ width: `${progressPercentage}%` }}
                    ></div>
                  </div>
                </div>

                {/* Funding Info */}
                <div className="mb-6">
                  <div className="text-2xl font-bold text-gray-900 mb-1">
                    {formatCurrency(campaign.raised_amount)}
                  </div>
                  <div className="text-gray-600 mb-4">
                    raised of {formatCurrency(campaign.goal_amount)} goal
                  </div>
                </div>

                {/* Donation Form */}
                {progressPercentage < 100 && daysRemaining > 0 && (
                  <div className="mb-6">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Donation Amount
                    </label>
                    <div className="relative">
                      <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">$</span>
                      <input
                        type="number"
                        value={donationAmount}
                        onChange={(e) => setDonationAmount(e.target.value)}
                        className="w-full pl-8 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="Enter amount"
                        min="1"
                      />
                    </div>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="space-y-3">
                  {progressPercentage >= 100 ? (
                    <div className="text-center py-4">
                      <div className="flex items-center justify-center gap-2 text-green-600 mb-2">
                        <Target className="h-5 w-5" />
                        <span className="font-semibold">Campaign Funded!</span>
                      </div>
                      <p className="text-sm text-gray-600">This campaign has reached its goal.</p>
                    </div>
                  ) : daysRemaining === 0 ? (
                    <div className="text-center py-4">
                      <div className="text-red-600 font-semibold mb-2">Campaign Ended</div>
                      <p className="text-sm text-gray-600">This campaign is no longer accepting donations.</p>
                    </div>
                  ) : (
                    <button
                      onClick={handleDonate}
                      disabled={!donationAmount || donationAmount <= 0}
                      className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                    >
                      Donate Now
                    </button>
                  )}
                  
                  <div className="flex gap-2">
                    <button className="flex-1 border border-gray-300 text-gray-700 py-2 px-4 rounded-lg font-medium hover:bg-gray-50 transition-colors">
                      <Share2 className="h-4 w-4 inline mr-2" />
                      Share
                    </button>
                    <button className="flex-1 border border-gray-300 text-gray-700 py-2 px-4 rounded-lg font-medium hover:bg-gray-50 transition-colors">
                      <Heart className="h-4 w-4 inline mr-2" />
                      Follow
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}