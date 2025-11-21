import { useState } from "react";
import { Button } from "@/Components/ui/button";
import { Textarea } from "@/Components/ui/textarea";
import { Card, CardContent } from "@/Components/ui/card";
import { Avatar, AvatarFallback } from "@/Components/ui/avatar";
import { Star, Edit2, Trash2, Send, Loader2, MessageSquare } from "lucide-react";
import {
  useProductComments,
  useCreateComment,
  useUpdateComment,
  useDeleteComment,
} from "@/hooks/useComment";
import { toast } from "sonner";
import { useAuthStore } from "@/Zustand/Auth/AuthState";
import { Link } from "react-router-dom";

interface CommentSectionProps {
  productId: number;
}

const CommentSection = ({ productId }: CommentSectionProps) => {
  const { user } = useAuthStore();
  const { data: commentsData, isLoading } = useProductComments(productId);
  const createCommentMutation = useCreateComment();
  const updateCommentMutation = useUpdateComment();
  const deleteCommentMutation = useDeleteComment();

  const [newComment, setNewComment] = useState("");
  const [newRating, setNewRating] = useState(0);
  const [editingCommentId, setEditingCommentId] = useState<number | null>(null);
  const [editContent, setEditContent] = useState("");
  const [editRating, setEditRating] = useState(0);

  const handleSubmitComment = async () => {
    if (!newComment.trim()) {
      toast.error("Please enter a Comment !");
      return;
    }

    if (!user) {
      toast.error("Please Login to Comment !");
      return;
    }

    try {
      await createCommentMutation.mutateAsync({
        product_id: productId,
        content: newComment,
        rating: newRating || undefined,
      });
      setNewComment("");
      setNewRating(0);
      toast.success("Comment posted successfully !");
    } catch (err) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error?.response?.data?.detail || "Failed to post comment !");
    }
  };

  const handleEditComment = (commentId: number, content: string, rating: number | null) => {
    setEditingCommentId(commentId);
    setEditContent(content);
    setEditRating(rating || 0);
  };

  const handleUpdateComment = async (commentId: number) => {
    if (!editContent.trim()) {
      toast.error("Please enter a Comment !");
      return;
    }

    try {
      await updateCommentMutation.mutateAsync({
        commentId,
        data: {
          content: editContent,
          rating: editRating || undefined,
        },
      });
      setEditingCommentId(null);
      setEditContent("");
      setEditRating(0);
      toast.success("Comment updated successfully !");
    } catch (err) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error?.response?.data?.detail || "Failed to update Comment !");
    }
  };

  const handleDeleteComment = async (commentId: number) => {
    toast.warning("Are you sure?", {
      description: "",
      action: {
        label: "Yes, Delete Comment",
        onClick: async () => {
          try {
            await deleteCommentMutation.mutateAsync(commentId);
            toast.success("Comment deleted successfully", {
              description: `Comment #${commentId} has been deleted.`,
            });
          } catch (err) {
            const error = err as { response?: { data?: { detail?: string } } };
            toast.error(error?.response?.data?.detail || "Failed to delete comment !");
          }
        },
      },
      cancel: {
        label: "Keep Comment",
        onClick: () => {
          toast.info("Comment deletion cancelled");
        },
      },
    });
  };

  const renderStars = (rating: number, interactive: boolean, onRate?: (rating: number) => void) => {
    return (
      <div className="flex gap-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            type="button"
            onClick={() => interactive && onRate && onRate(star)}
            disabled={!interactive}
            className={`${interactive ? "cursor-pointer hover:scale-110" : "cursor-default"} transition-transform`}
          >
            <Star
              className={`w-5 h-5 ${star <= rating
                  ? "text-yellow-400 fill-current"
                  : "text-gray-600"
                }`}
            />
          </button>
        ))}
      </div>
    );
  };

  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    } catch {
      return "Invalid date format";
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center py-8">
        <Loader2 className="w-8 h-8 text-blue-400 animate-spin" />
      </div>
    );
  }

  const comments = commentsData?.comments || [];
  const averageRating = commentsData?.average_rating || 0;
  const totalComments = commentsData?.total_comments || 0;

  return (
    <div className="mt-16">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-2xl font-bold text-blue-400 flex items-center gap-2">
            <MessageSquare className="w-6 h-6" />
            Customer Reviews
          </h2>
          <div className="flex items-center gap-4 mt-2">
            {averageRating > 0 && (
              <>
                <div className="flex items-center gap-1">
                  {renderStars(Math.round(averageRating), false)}
                </div>
                <span className="text-gray-300">
                  {averageRating.toFixed(1)} out of 5
                </span>
              </>
            )}
            <span className="text-gray-400">({totalComments} reviews)</span>
          </div>
        </div>
      </div>

      {/* Add Comment */}
      {user ? (
        <Card className="bg-gray-800 border-gray-700 mb-8">
          <CardContent className="p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Write a Review</h3>
            <div className="space-y-4">
              <div>
                <label className="text-sm text-gray-400 mb-2 block">
                  Your Rating (Optional)
                </label>
                {renderStars(newRating, true, setNewRating)}
              </div>
              <Textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Share your thoughts about this product..."
                className="bg-gray-900 border-gray-600 text-white placeholder-gray-500 min-h-[100px]"
                maxLength={1000}
              />
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-400">
                  {newComment.length}/1000 characters
                </span>
                <Button
                  onClick={handleSubmitComment}
                  disabled={createCommentMutation.isPending || !newComment.trim()}
                  className="bg-blue-600 hover:bg-blue-700 text-white cursor-pointer"
                >
                  {createCommentMutation.isPending ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Posting...
                    </>
                  ) : (
                    <>
                      <Send className="w-4 h-4 mr-2" />
                      Post Review
                    </>
                  )}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      ) : (
        <Card className="bg-gray-800 border-gray-700 mb-8">
          <CardContent className="p-6 text-center">
            <p className="text-gray-400 mb-4">Please login to write a review</p>
            <Link to={`/login`}>
              <Button className="bg-blue-600 hover:bg-blue-700 text-white cursor-pointer">
                Login
              </Button>
            </Link>
          </CardContent>
        </Card>
      )}

      {/* Comments List */}
      <div className="space-y-4">
        {comments.length === 0 ? (
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-8 text-center">
              <MessageSquare className="w-12 h-12 text-gray-600 mx-auto mb-4" />
              <p className="text-gray-400">No reviews yet. Be the first to review!</p>
            </CardContent>
          </Card>
        ) : (
          comments.map((comment) => (
            <Card key={comment.id} className="bg-gray-800 border-gray-700">
              <CardContent className="p-6">
                {editingCommentId === comment.id ? (
                  // Edit Mode \\
                  <div className="space-y-4">
                    <div>
                      <label className="text-sm text-gray-400 mb-2 block">
                        Your Rating (Optional)
                      </label>
                      {renderStars(editRating, true, setEditRating)}
                    </div>
                    <Textarea
                      value={editContent}
                      onChange={(e) => setEditContent(e.target.value)}
                      className="bg-gray-900 border-gray-600 text-white min-h-[100px]"
                      maxLength={1000}
                    />
                    <div className="flex gap-2">
                      <Button
                        onClick={() => handleUpdateComment(comment.id)}
                        disabled={updateCommentMutation.isPending}
                        className="bg-blue-600 hover:bg-blue-700 text-white"
                      >
                        {updateCommentMutation.isPending ? (
                          <>
                            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                            Updating...
                          </>
                        ) : (
                          "Save Changes"
                        )}
                      </Button>
                      <Button
                        onClick={() => {
                          setEditingCommentId(null);
                          setEditContent("");
                          setEditRating(0);
                        }}
                        variant="outline"
                        className="border-gray-600 text-gray-300"
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                ) : (
                  // View Mode \\
                  <>
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-start gap-3">
                        <Avatar className="h-10 w-10 bg-blue-600">
                          <AvatarFallback className="bg-blue-600 text-white">
                            {comment.username?.charAt(0).toUpperCase() || "U"}
                          </AvatarFallback>
                        </Avatar>
                        <div>
                          <p className="font-semibold text-white">
                            {comment.username || "Anonymous"}
                          </p>
                          <p className="text-sm text-gray-400">
                            {formatDate(comment.created_at)}
                          </p>
                          {comment.rating && (
                            <div className="mt-1">
                              {renderStars(comment.rating, false)}
                            </div>
                          )}
                        </div>
                      </div>
                      {user && user.id === comment.user_id && (
                        <div className="flex gap-2">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() =>
                              handleEditComment(comment.id, comment.content, comment.rating)
                            }
                            className="border-gray-600 text-gray-300 hover:bg-gray-700"
                          >
                            <Edit2 className="w-4 h-4" />
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleDeleteComment(comment.id)}
                            disabled={deleteCommentMutation.isPending}
                            className="border-red-600 text-red-400 hover:bg-red-900/20"
                          >
                            {deleteCommentMutation.isPending ? (
                              <Loader2 className="w-4 h-4 animate-spin" />
                            ) : (
                              <Trash2 className="w-4 h-4" />
                            )}
                          </Button>
                        </div>
                      )}
                    </div>
                    <p className="text-gray-300 leading-relaxed">{comment.content}</p>
                  </>
                )}
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

export default CommentSection;