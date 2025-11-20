import { useState } from 'react';
import { Card, CardContent } from '@/Components/ui/card';
import { Button } from '@/Components/ui/button';
import { toast } from 'sonner';
import {
  Eye,
  EyeOff
} from 'lucide-react';
import { GiClown } from "react-icons/gi";

export const Terms = () => {
  const [showSecret, setShowSecret] = useState(false);

  const handleSecretClick = () => {
    setShowSecret(!showSecret);
    toast.error('Why did you click? there is absolutely nothing here', {
      duration: 3000,
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900 py-8 relative overflow-hidden">

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">

        <div className="space-y-6">

          <Card className="bg-gradient-to-r from-slate-800/50 to-blue-900/50 border-blue-500 border-2 transform hover:scale-105 transition-transform duration-300">
            <CardContent className="p-8 text-center">
              <GiClown className="h-20 w-20 mx-auto mb-4 text-blue-400 animate-bounce" />
              <h2 className="text-3xl font-bold text-white mb-4">
                NOTHING TO SEE HERE !
              </h2>
            </CardContent>
          </Card>


          <Card className="bg-gradient-to-r from-blue-900/50 to-slate-800/50 border-cyan-500 border-2">
            <CardContent className="p-8 text-center">
              <div className="mb-4">
                <Button
                  onClick={handleSecretClick}
                  className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-bold text-lg px-8 py-6 cursor-pointer"
                >
                  {showSecret ? (
                    <>
                      <EyeOff className="h-5 w-5 mr-2" />
                      Hide the Secret
                      <EyeOff className="h-5 w-5 mr-2" />
                    </>
                  ) : (
                    <>
                      <Eye className="h-5 w-5 mr-2" />
                      Reveal the Secret Message
                      <Eye className="h-5 w-5 mr-2" />
                    </>
                  )}
                </Button>
              </div>

              {showSecret && (
                <div className="mt-6 p-6 bg-black/30 rounded-lg animate-fade-in">
                  <p className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-400 to-blue-500 mb-3">
                    CONGRATS!
                  </p>
                  <p className="text-slate-300 text-lg">
                    Why bother clicking ? There is absolutely nothing here
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

        </div>

      </div>
    </div>
  );
};