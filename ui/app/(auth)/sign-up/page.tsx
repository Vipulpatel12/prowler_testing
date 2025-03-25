import { AuthForm } from "@/components/auth/oss";
import { isGithubOAuthEnabled } from "@/lib/helper";
import { isGoogleOAuthEnabled } from "@/lib/helper";
import { SearchParamsProps } from "@/types";

const SignUp = ({ searchParams }: { searchParams: SearchParamsProps }) => {
  const invitationToken =
    typeof searchParams?.invitation_token === "string"
      ? searchParams.invitation_token
      : null;
  const emailId =
    typeof searchParams?.email === "string"
      ? searchParams.email
      : null;

  const user_name =
    typeof searchParams?.user_name === "string"
      ? searchParams.user_name
      : null;

  const company =
    typeof searchParams?.company === "string"
      ? searchParams.company
      : null;

  return (
    <AuthForm
      type="sign-up"
      invitationToken={invitationToken}
      emailId={emailId ?? ''}
      userName={user_name ?? ''}
      companyName={company ?? ''}
      isGoogleOAuthEnabled={isGoogleOAuthEnabled}
      isGithubOAuthEnabled={isGithubOAuthEnabled}
    />
  );
};

export default SignUp;
