clean_up ()
{
	echo "Clean up ..."
}

# register clean_up fuction
trap clean_up EXIT
